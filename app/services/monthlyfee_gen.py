from datetime import date
from sqlalchemy.orm import Session
from app.db.models import Student, TeachingAssignment, MonthlyFee, PaymentState

class MonthlyFeeService:
    def __init__(self, db: Session):
        self.db = db

    def generate_for_month(self, month: str):
        """
        Generate MonthlyFee rows for all students based on active assignments.
        month: string "YYYY-MM" e.g., "2026-02"
        """
        result = {"created": 0, "skipped": 0}

        # Fetch all students
        students = self.db.query(Student).all()
        print("Students in DB:", len(students))
        for student in students:
            print("here")
            # Check if fee for this month already exists
            existing_fee = (
                self.db.query(MonthlyFee)
                .filter(MonthlyFee.student_id == student.external_id)
                .filter(MonthlyFee.month == month)
                .first()
            )
            if existing_fee:
                result["skipped"] += 1
                continue

            # Sum active assignments for this student
            active_assignments = [
                a for a in student.assignments if getattr(a, "active", True)
            ]
            if not active_assignments:
                continue  # no fee to generate

            total_amount = sum(
                a.lessons_per_month * a.rate_per_lesson for a in active_assignments
            )

            # Compute due_date safely
            day = min(student.fee_due_day, 28)  # avoid invalid dates
            year, month_num = map(int, month.split("-"))
            due_date = date(year, month_num, day)

            fee = MonthlyFee(
                student_id=student.external_id,
                month=month,
                amount=total_amount,
                due_date=due_date,
                status=PaymentState.unpaid,
            )
            self.db.add(fee)
            result["created"] += 1

        self.db.commit()
        return result
