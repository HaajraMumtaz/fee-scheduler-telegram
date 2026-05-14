from fastapi import APIRouter, Depends, Query
from datetime import date
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.billing_orchestrator import BillingOrchestrator
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])


def get_orchestrator(db: Session = Depends(get_db)) -> BillingOrchestrator:
    return BillingOrchestrator(db)


@router.post("/month-start")
def generate_month_start_report(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    user: dict = Depends(get_current_user),
):
    period = date(year, month, 1)
    return {
        "type": "month_start",
        "period": period.isoformat(),
        "result": orchestrator.run_month_start(period),
    }


@router.post("/month-end")
def generate_month_end_report(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    user: dict = Depends(get_current_user),
):
    period = date(year, month, 1)
    return {
        "type": "month_end",
        "period": period.isoformat(),
        "result": orchestrator.run_payroll(period),
    }


@router.post("/daily-reminders")
def generate_daily_reminder_report(
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    user: dict = Depends(get_current_user),
):
    return {
        "type": "daily_reminders",
        "result": orchestrator.run_daily_reminders(),
    }