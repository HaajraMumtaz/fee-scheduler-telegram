from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
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

    

    def mark_paid(self, student_id: int, period: date, amount: float = 0):
        fee = (
            self.db.query(MonthlyFee)
            .filter(
                MonthlyFee.student_id == student_id,
                MonthlyFee.month == period.month
            )
            .first()
        )

        if not fee:
            return None

        # Create payment record
        payment = StudentPayment(
            student_id=student_id,
            amount=amount,
            paid_on=date.today()
        )

    
        fee.status = PaymentState.paid

        self.db.add(payment)
        self.db.commit()

        return payment

    

    def get_unpaid_students(self,today=None):
        today = today or date.today()

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