from datetime import date,datetime
from sqlalchemy.orm import Session,func
from app.db.models import (
    Teacher,
    TeachingAssignment,
    TeachingException
)

class PayrollCalculator:

    def __init__(self, db: Session):
        self.db = db

    def calculate_teacher_payroll(self, teacher_id: int, period: date):

        s
        if period.month == 12:
            end_date = period.replace(year=period.year + 1, month=1)
        else:
            end_date = period.replace(month=period.month + 1)

        assignments = (
            self.db.query(TeachingAssignment)
            .filter(
                TeachingAssignment.teacher_id == teacher_id,
                TeachingAssignment.active == True
            )
            .all()
        )

        total_amount = 0
        breakdown = []

        for assignment in assignments:

            base_lessons = assignment.lessons_per_month

            missed_lessons = (
                self.db.query(
                    func.coalesce(func.sum(TeachingException.lessons_missed), 0)
                )
                .filter(
                    TeachingException.assignment_id == assignment.id,
                    TeachingException.date >= start_date,
                    TeachingException.date < end_date
                )
                .scalar()
            )

            actual_lessons = max(base_lessons - missed_lessons, 0)
            payout = actual_lessons * assignment.rate_per_lesson
            total_amount += payout

            breakdown.append({
                "assignment_id": assignment.id,
                "student_id": assignment.student_id,
                "subject": assignment.subject,
                "lessons_taught": actual_lessons,
                "rate_per_lesson": assignment.rate_per_lesson,
                "amount": payout
            })

        return {
            "teacher_id": teacher_id,
            "month": period.month,
            "total_amount": total_amount,
            "breakdown": breakdown
        }
    def generate_monthly_payroll(self, month: str):
        teachers = self.db.query(Teacher).all()

        payrolls = []

        for teacher in teachers:
            result = self.calculate_teacher_payroll(teacher.id, month)
            payrolls.append(result)

        return payrolls