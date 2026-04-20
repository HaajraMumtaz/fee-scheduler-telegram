from fastapi import APIRouter
from datetime import date

from app.billing_orchestrator import BillingOrchestrator

router = APIRouter(prefix="/api/payroll")

orchestrator = None


@router.post("/run")
def run_payroll():
    return orchestrator.run_payroll(date.today())