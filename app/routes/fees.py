from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import MonthlyFee, PaymentState
from app.deps import get_monthly_fee_service
from app.services.monthlyfee_gen import MonthlyFeeService
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/fees", tags=["Fees"])


@router.get("/")
def list_fees(
    student_id: int | None = None,
    status: PaymentState | None = None,
    year: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    q = db.query(MonthlyFee)

    if student_id:
        q = q.filter(MonthlyFee.student_id == student_id)
    if status:
        q = q.filter(MonthlyFee.status == status)
    if year:
        q = q.filter(MonthlyFee.year == year)
    if month:
        q = q.filter(MonthlyFee.month == month)

    return {
        "fees": [
            {
                "id": f.id,
                "student_id": f.student_id,
                "year": f.year,
                "month": f.month,
                "amount": f.amount,
                "due_date": f.due_date.isoformat(),
                "status": f.status.value,
                "paid_on": f.paid_on.isoformat() if f.paid_on else None,
            }
            for f in q.all()
        ]
    }


@router.post("/generate")
def generate_fees(
    year: int | None = None,
    month: int | None = None,
    svc: MonthlyFeeService = Depends(get_monthly_fee_service),
    user: dict = Depends(get_current_user),
):
    today = date.today()
    y = year or today.year
    m = month or today.month

    if not (1 <= m <= 12):
        raise HTTPException(status_code=400, detail="Invalid month")

    return svc.generate_for_month(date(y, m, 1))


@router.post("/{fee_id}/dismiss")
def dismiss_fee(
    fee_id: int,
    until: date,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    fee = db.query(MonthlyFee).filter(MonthlyFee.id == fee_id).first()
    if not fee:
        raise HTTPException(status_code=404, detail="Fee not found")

    if fee.status == PaymentState.paid:
        raise HTTPException(status_code=400, detail="Cannot dismiss paid fee")

    fee.dismissed_until = until
    db.commit()
    return {"fee_id": fee_id, "dismissed_until": until.isoformat()}