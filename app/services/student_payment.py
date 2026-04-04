from datetime import date
from sqlalchemy.orm import Session,extract,func, or_
from app.db.models import Student, StudentPayment, PaymentReminder, PaymentState,MonthlyFee


class StudentPaymentService:
    """
    Service layer responsible for handling student payments .
    Encapsulates business logic related to payment state and queries.
    """
    def __init__(self, db: Session):
        """
        Initialize the service with a database session.

        :param db: SQLAlchemy database session
        """
        self.db = db

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

    

    def get_unpaid_students(self):
        today = date.today()

        return (
            self.db.query(
                Student.name,
                MonthlyFee.student_id,
                func.count(MonthlyFee.id)
            )
            .join(Student)
            .filter(
                MonthlyFee.status != PaymentState.paid,
                MonthlyFee.due_date <= today,
                or_(
                    MonthlyFee.dismissed_until == None,
                    MonthlyFee.dismissed_until <= today
                )
            )
            .group_by(MonthlyFee.student_id)
            .all()
        )