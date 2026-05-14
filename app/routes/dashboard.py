from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.engine import get_db
from app.db.models import (
    Student, Teacher, MonthlyFee,
    PaymentState, PayrollRun, PayrollStatus,
)
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api", tags=["Dashboard"])


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    today = date.today()

    overdue_filter = (
        (MonthlyFee.status != PaymentState.paid)
        & (MonthlyFee.due_date <= today)
    )

    return {
        "total_students": db.query(func.count(Student.id)).scalar(),
        "active_teachers": (
            db.query(func.count(Teacher.id))
            .filter(Teacher.status == "active")
            .scalar()
        ),
        "overdue_fees_count": (
            db.query(func.count(MonthlyFee.id))
            .filter(overdue_filter)
            .scalar()
        ),
        "overdue_fees_amount": float(
            db.query(func.coalesce(func.sum(MonthlyFee.amount), 0))
            .filter(overdue_filter)
            .scalar() or 0
        ),
        "pending_payrolls": (
            db.query(func.count(PayrollRun.id))
            .filter(PayrollRun.status == PayrollStatus.draft)
            .scalar()
        ),
        "as_of": today.isoformat(),
    }