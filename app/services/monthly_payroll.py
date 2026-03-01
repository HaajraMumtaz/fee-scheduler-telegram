from sqlalchemy.orm import Session
from app.db.models import (
    Teacher,
    PayrollRun,
    PayrollStatus,
)
from .payroll_calc import PayrollCalculator


class PayrollService:

    def __init__(self, db: Session):
        self.db = db
        self.calculator = PayrollCalculator(db)

    def generate_payroll_for_month(self, month: str):

        teachers = (
            self.db.query(Teacher)
            .filter(Teacher.status == "active")
            .all()
        )

        payrolls_created = []

        for teacher in teachers:

            result = self.calculator.calculate_teacher_payroll(
                teacher_id=teacher.id,
                month=month
            )

            if result["total_amount"] > 0:
                payroll = PayrollRun(
                    teacher_id=teacher.id,
                    month=month,
                    total_amount=result["total_amount"],
                    status=PayrollStatus.draft
                )

                self.db.add(payroll)
                payrolls_created.append(payroll)

        self.db.commit()

        return payrolls_created