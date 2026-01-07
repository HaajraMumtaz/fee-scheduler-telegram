from datetime import date
from sqlalchemy.orm import Session
from app.db.models import Student, StudentPayment, PaymentReminder, PaymentState


class StudentPaymentService:
    def __init__(self, db: Session):
        self.db = db

    def send_reminder(self, student_id: int, channel="telegram"):
        student = self.db.get(Student, student_id)
        if not student or student.payment_state == PaymentState.paid:
            return None

        reminder_count = (
            self.db.query(PaymentReminder)
            .filter(PaymentReminder.student_id == student_id)
            .count()
        )

        reminder = PaymentReminder(
            student_id=student_id,
            sent_on=date.today(),
            channel=channel,
            message_number=reminder_count + 1
        )

        self.db.add(reminder)
        self.db.commit()

        return reminder

    def mark_paid(self, student_id: int, amount: float):
        student = self.db.get(Student, student_id)
        if not student:
            return None

        payment = StudentPayment(
            student_id=student_id,
            amount=amount,
            paid_on=date.today()
        )

        student.payment_state = PaymentState.paid

        self.db.add(payment)
        self.db.commit()

        return payment

    def unpaid_students(self):
        return (
            self.db.query(Student)
            .filter(Student.payment_state == PaymentState.unpaid)
            .all()
        )
