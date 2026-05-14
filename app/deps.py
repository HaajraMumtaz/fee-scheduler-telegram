"""
FastAPI dependency-injection helpers.

Usage in a route:
    from app.deps import get_student_payment_service

    @router.get("/unpaid")
    def unpaid(svc: StudentPaymentService = Depends(get_student_payment_service)):
        ...
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.services.student_payment import StudentPaymentService
from app.services.monthly_payroll import PayrollService
from app.services.monthlyfee_gen import MonthlyFeeService
from app.services.payment_reminder import PaymentReminderService
from app.db.repositories.student_repo import StudentRepository
from app.db.repositories.teacher_repo import TeacherRepository
from app.db.repositories.assignment_repo import TeachingAssignmentRepository


# ── Repository helpers ────────────────────────────────────────────────────────

def get_student_repo(db: Session = Depends(get_db)) -> StudentRepository:
    return StudentRepository(db)


def get_teacher_repo(db: Session = Depends(get_db)) -> TeacherRepository:
    return TeacherRepository(db)


def get_assignment_repo(db: Session = Depends(get_db)) -> TeachingAssignmentRepository:
    return TeachingAssignmentRepository(db)


# ── Service helpers ───────────────────────────────────────────────────────────

def get_student_payment_service(db: Session = Depends(get_db)) -> StudentPaymentService:
    return StudentPaymentService(db)


def get_payroll_service(db: Session = Depends(get_db)) -> PayrollService:
    return PayrollService(db)


def get_monthly_fee_service(db: Session = Depends(get_db)) -> MonthlyFeeService:
    return MonthlyFeeService(db)


def get_payment_reminder_service(
    db: Session = Depends(get_db),
    sps: StudentPaymentService = Depends(get_student_payment_service),
) -> PaymentReminderService:
    return PaymentReminderService(db, sps)
