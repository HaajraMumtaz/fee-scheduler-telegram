from datetime import date
from sqlalchemy.orm import Session
from app.db.models import (
    Teacher,
    TeachingAssignment,
    TeachingException
)

class PayrollCalculator:
    def __init__(self, db: Session):
        self.db = db

    def calculate_teacher_payroll(self, teacher_id: int, month: str):
        """
        month: "YYYY-MM"
        Returns:
        {
            "teacher_id": int,
            "month": str,
            "total_amount": float,
            "breakdown": list[dict]
        }
        """

        assignments = (
            self.db.query(TeachingAssignment)
            .filter(TeachingAssignment.teacher_id == teacher_id)
            .all()
        )

        total_amount = 0.0
        breakdown = []

        for assignment in assignments:
            # Base lessons
            base_lessons = assignment.lessons_per_month

            # Missed lessons for this assignment in this month
            missed = (
                self.db.query(TeachingException)
                .filter(TeachingException.assignment_id == assignment.id)
                .filter(TeachingException.date.like(f"{month}%"))
                .all()
            )

            lessons_missed = sum(e.lessons_missed for e in missed)
            lessons_taught = max(base_lessons - lessons_missed, 0)

            amount = lessons_taught * assignment.rate_per_lesson
            total_amount += amount

            breakdown.append({
                "assignment_id": assignment.id,
                "student_id": assignment.student_id,
                "subject": assignment.subject,
                "lessons_taught": lessons_taught,
                "rate_per_lesson": assignment.rate_per_lesson,
                "amount": amount
            })

        return {
            "teacher_id": teacher_id,
            "month": month,
            "total_amount": total_amount,
            "breakdown": breakdown
        }
