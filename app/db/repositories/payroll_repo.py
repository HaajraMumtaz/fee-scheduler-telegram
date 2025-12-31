from sqlalchemy.orm import Session
from datetime import date
from app.db.models import (
    PayrollRun,
    TeachingAssignment,
    TeachingException,
    PayrollStatus
)
class PayrollRepository:
    def __init__(self, db: Session):
        """
        db: injected SQLAlchemy session
        """
        self.db = db
    def create_monthly_payroll(self, teacher_id: int, month: str):
        """
        Creates a payroll snapshot for a teacher for a given month.
        month format: 'YYYY-MM'
        """

        assignments = (
            self.db.query(TeachingAssignment)
            .filter(TeachingAssignment.teacher_id == teacher_id)
            .all()
        )

        total_amount = 0.0

        for assignment in assignments:
            expected_lessons = assignment.lessons_per_month

            exceptions = (
                self.db.query(TeachingException)
                .filter(TeachingException.assignment_id == assignment.id)
                .filter(TeachingException.date.like(f"{month}%"))
                .all()
            )

            missed_lessons = sum(e.lessons_missed for e in exceptions)
            payable_lessons = max(expected_lessons - missed_lessons, 0)

            total_amount += payable_lessons * assignment.rate_per_lesson

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

    def approve(self, payroll_id: int):
        payroll = self.db.get(PayrollRun, payroll_id)

        if not payroll:
            return None

        payroll.status = PayrollStatus.approved
        self.db.commit()
        return payroll
    def mark_paid(self, payroll_id: int):
        payroll = self.db.get(PayrollRun, payroll_id)

        if not payroll:
            return None

        payroll.status = PayrollStatus.paid
        self.db.commit()
        return payroll

