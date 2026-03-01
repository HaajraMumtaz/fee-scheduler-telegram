from datetime import date
from sqlalchemy import extract
from app.db.models import MonthlyFee, PaymentReminder, PaymentState


def send_reminder(self, student_id: int, channel="telegram"):
    '''this service '''
    today = date.today()

    # 1️⃣ Check if student has unpaid & due monthly fees
    months_due = (
        self.db.query(MonthlyFee)
        .filter(
            MonthlyFee.student_id == student_id,
            MonthlyFee.status != PaymentState.paid,
            MonthlyFee.due_date <= today,
        )
        .count()
    )

    if months_due == 0:
        return None  # Nothing to remind

    # 2️⃣ Count reminders sent THIS calendar month
    reminder_count = (
        self.db.query(PaymentReminder)
        .filter(
            PaymentReminder.student_id == student_id,
            extract("month", PaymentReminder.sent_on) == today.month,
            extract("year", PaymentReminder.sent_on) == today.year,
        )
        .count()
    )

    # 3️⃣ Create new reminder
    reminder = PaymentReminder(
        student_id=student_id,
        sent_on=today,
        channel=channel,
        message_number=reminder_count + 1
    )

    self.db.add(reminder)
    self.db.commit()

    return reminder 