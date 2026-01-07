from datetime import date
from sqlalchemy.orm import Session

from app.db.engine import SessionLocal
from app.db.init_db import init_db
from app.db.models import (
    Teacher,
    Student,
    TeachingAssignment,
    TeachingException
)
from app.services.payroll_calc import PayrollCalculator


def main():
    print("🔄 Resetting database...")
    init_db()
    print("✅ Database ready\n")

    db: Session = SessionLocal()

    try:
        # 1️⃣ Create teacher
        print("1️⃣ Creating teacher")
        teacher = Teacher(name="Ustad Ali")
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        print(f"Teacher ID: {teacher.id}\n")

        # 2️⃣ Create students
        print("2️⃣ Creating students")
        s1 = Student(
            name="Ali",
            fee_due_date=date(2025, 1, 10)
        )
        s2 = Student(
            name="Ahmed",
            fee_due_date=date(2025, 1, 10)
        )

        db.add_all([s1, s2])
        db.commit()
        db.refresh(s1)
        db.refresh(s2)

        print(f"Students: {s1.id}, {s2.id}\n")

        # 3️⃣ Teaching assignments
        print("3️⃣ Creating teaching assignments")
        a1 = TeachingAssignment(
            student_id=s1.id,
            teacher_id=teacher.id,
            subject="Math",
            lessons_per_month=8,
            rate_per_lesson=500
        )

        a2 = TeachingAssignment(
            student_id=s2.id,
            teacher_id=teacher.id,
            subject="Physics",
            lessons_per_month=8,
            rate_per_lesson=500
        )

        db.add_all([a1, a2])
        db.commit()
        db.refresh(a1)
        db.refresh(a2)

        # 4️⃣ Teaching exception (teacher on leave)
        print("4️⃣ Adding teaching exception")
        exception = TeachingException(
            assignment_id=a1.id,
            date=date(2025, 1, 15),
            reason="Teacher on leave",
            lessons_missed=2
        )

        db.add(exception)
        db.commit()

        # 5️⃣ Payroll calculation
        print("5️⃣ Calculating payroll\n")
        calculator = PayrollCalculator(db)
        payroll = calculator.calculate_teacher_payroll(
            teacher_id=teacher.id,
            month="2025-01"
        )

        print("📄 PAYROLL PREVIEW")
        print(payroll)

    finally:
        db.close()


if __name__ == "__main__":
    main()
