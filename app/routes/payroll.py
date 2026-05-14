from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.billing_orchestrator import BillingOrchestrator
from app.db.models import PayrollStatus, PayrollRun
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/payroll", tags=["Payroll"])


def get_orchestrator(db: Session = Depends(get_db)) -> BillingOrchestrator:
    return BillingOrchestrator(db)


def get_payroll_or_404(db: Session, payroll_id: int) -> PayrollRun:
    run = db.query(PayrollRun).filter(PayrollRun.id == payroll_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Payroll run not found")
    return run


@router.post("/run")
def run_payroll(
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    user: dict = Depends(get_current_user),
):
    return orchestrator.run_payroll(date.today())


@router.get("/")
def list_payrolls(
    month: str | None = None,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    q = db.query(PayrollRun)
    if month:
        q = q.filter(PayrollRun.month == month)

    return {
        "payrolls": [
            {
                "id": r.id,
                "teacher_id": r.teacher_id,
                "month": r.month,
                "total_amount": r.total_amount,
                "status": r.status.value,
            }
            for r in q.all()
        ]
    }


@router.post("/{payroll_id}/approve")
def approve_payroll(
    payroll_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    run = get_payroll_or_404(db, payroll_id)

    if run.status != PayrollStatus.draft:
        raise HTTPException(status_code=400, detail="Only draft payroll can be approved")

    run.status = PayrollStatus.approved
    db.commit()
    return {"id": payroll_id, "status": "approved"}


@router.post("/{payroll_id}/mark-paid")
def mark_payroll_paid(
    payroll_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    run = get_payroll_or_404(db, payroll_id)

    if run.status != PayrollStatus.approved:
        raise HTTPException(status_code=400, detail="Only approved payroll can be marked as paid")

    run.status = PayrollStatus.paid 
    db.commit()
    return {"id": payroll_id, "status": "paid"}