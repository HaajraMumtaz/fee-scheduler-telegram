from sqlalchemy.orm import Session
from datetime import date
from app.db.models import (
    PayrollRun,
    PayrollStatus
)
from app.services.payroll_calc import PayrollCalculator

class PayrollRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, teacher_id: int, month: str, total_amount: float):
        payroll = PayrollRun(
            teacher_id=teacher_id,
            month=month,
            total_amount=total_amount,
            status=PayrollStatus.draft
        )
        self.db.add(payroll)
        self.db.commit()
        self.db.refresh(payroll)
        return payroll

    def get_by_id(self, payroll_id: int):
        return self.db.get(PayrollRun, payroll_id)

    def approve(self, payroll_id: int):
        payroll = self.get_by_id(payroll_id)
        if not payroll:
            return None

        payroll.status = PayrollStatus.approved
        self.db.commit()
        return payroll

    def mark_paid(self, payroll_id: int):
        payroll = self.get_by_id(payroll_id)
        if not payroll:
            return None

        payroll.status = PayrollStatus.paid
        self.db.commit()
        return payroll
    from sqlalchemy.orm import Session

    def preview_payroll(db: Session, teacher_id: int, month: str):
        # start a transaction
        with db.begin_nested():  # begin a subtransaction
            payroll = PayrollCalculator.calculate_teacher_payroll(db, teacher_id, month)
            # do NOT commit
            return payroll  # just return the calculated object
        # exiting the block rolls back automatically
