from datetime import date
from sqlalchemy.orm import Session,extract
from app.db.models import Student, StudentPayment, PaymentReminder, PaymentState


class StudentPaymentService:
    """
    Service layer responsible for handling student payments and reminders.
    Encapsulates business logic related to payment state, reminders, and queries.
    """
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.

        :param db: SQLAlchemy database session
        """
        self.db = db


    def send_reminder(self, student_id: int, channel="telegram"):
        student = self.db.get(Student, student_id)

        if not student or student.payment_state == PaymentState.paid:
            return None

        today = date.today()

        reminder_count = (
            self.db.query(PaymentReminder)
            .filter(
                PaymentReminder.student_id == student_id,
                extract('month', PaymentReminder.sent_on) == today.month,
                extract('year', PaymentReminder.sent_on) == today.year,
            )
            .count()
        )

        reminder = PaymentReminder(
            student_id=student_id,
            sent_on=today,
            channel=channel,
            message_number=reminder_count + 1
        )

        self.db.add(reminder)
        self.db.commit()

        return reminder


    def mark_paid(self, student_id: int, amount: float):
        """
        Mark a student as paid and record their payment.

        Creates a StudentPayment record and updates the student's payment state
        to 'paid'.

        :param student_id: ID of the student
        :param amount: Amount paid by the student
        :return: Created StudentPayment object or None if student not found
        """
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
        """
        Retrieve all students who currently have an unpaid payment state.

        :return: List of Student objects with payment_state == unpaid
        """
        return (
            self.db.query(Student)
            .filter(Student.payment_state == PaymentState.unpaid)
            .all()
        )
