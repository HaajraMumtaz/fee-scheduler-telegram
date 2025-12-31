from datetime import date
from app.db.engine import SessionLocal
from app.db.init_db import init_db
from app.db.models import Student, Teacher, TeachingAssignment, TeachingException
from app.db.repositories.student_repo import StudentRepository
from app.db.repositories.teacher_repo import TeacherRepository
from app.db.repositories.assignment_repo import TeachingAssignmentRepository
from app.db.repositories.exception_repo import TeachingExceptionRepository
from app.db.repositories.payroll_repo import PayrollRepository

# Initialize DB
init_db()

db = SessionLocal()
teacher_repo = TeacherRepository(db)
student_repo = StudentRepository(db)

teacher = teacher_repo.create(
    Teacher(name="Ali Khan")
)

student = student_repo.create(
    Student(
        name="Ahmed",
        fee_due_date=date(2025, 1, 10),
        poc_name="Parent Ahmed",
        poc_phone="0300-0000000"
    )
)

print("Teacher:", teacher.id, teacher.name)
print("Student:", student.id, student.name)
assignment_repo = TeachingAssignmentRepository(db)

assignment = assignment_repo.create(
    TeachingAssignment(
        student_id=student.id,
        teacher_id=teacher.id,
        subject="Math",
        lessons_per_month=8,
        rate_per_lesson=1500
    )
)

print("Assignment ID:", assignment.id)
exception_repo = TeachingExceptionRepository(db)

exception_repo.create(
    assignment_id=assignment.id,
    exception_date=date(2025, 1, 15),
    reason="Teacher on leave",
    lessons_missed=2
)


print("Exception recorded")
payroll_repo = PayrollRepository(db)

payroll = payroll_repo.create_monthly_payroll(
    teacher_id=teacher.id,
    month="2025-01"
)

print("Payroll amount:", payroll.total_amount)
print("Payroll status:", payroll.status)
payroll_repo.approve(payroll.id)
payroll_repo.mark_paid(payroll.id)

# final = payroll_repo.get_by_teacher_month(teacher.id, "2025-01")
print("Final payroll status:", payroll.status)
