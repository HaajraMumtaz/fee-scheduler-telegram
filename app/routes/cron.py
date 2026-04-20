from fastapi import APIRouter
from datetime import date

from app.billing_orchestrator import BillingOrchestrator

router = APIRouter(prefix="/api/cron")

orchestrator = None


@router.post("/month-start")
def month_start():
    return orchestrator.run_month_start(date.today())


@router.post("/daily-reminders")
def daily_reminders():
    return orchestrator.run_daily_reminders()


@router.post("/month-end")
def month_end():
    return orchestrator.run_payroll(date.today())