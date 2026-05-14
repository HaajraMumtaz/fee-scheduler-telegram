import os

from fastapi import APIRouter, Header, HTTPException, Depends
from datetime import date
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.billing_orchestrator import BillingOrchestrator

router = APIRouter(prefix="/api/cron", tags=["Cron"])

CRON_SECRET = os.getenv("CRON_SECRET", "SUPER_SECRET_CRON_KEY")

def verify_cron_token(x_cron_key: str = Header(...)):
    if x_cron_key != CRON_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")


def get_orchestrator(
    db: Session = Depends(get_db),
) -> BillingOrchestrator:
    return BillingOrchestrator(db)

@router.post("/month-start")
def month_start(
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    _: None = Depends(verify_cron_token),
):
    return orchestrator.run_month_start(date.today())


@router.post("/daily-reminders")
def daily_reminders(
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    _: None = Depends(verify_cron_token),
):
    return orchestrator.run_daily_reminders()


@router.post("/month-end")
def month_end(
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    _: None = Depends(verify_cron_token),
):
    return orchestrator.run_payroll(date.today())