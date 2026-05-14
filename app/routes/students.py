from fastapi import APIRouter, Depends, HTTPException
from datetime import date

from app.deps import get_student_payment_service
from app.services.student_payment import StudentPaymentService
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("/unpaid")
def get_unpaid_students(
    svc: StudentPaymentService = Depends(get_student_payment_service),
    user: dict = Depends(get_current_user),
):
    results = svc.get_unpaid_students()

    return {
        "students": [
            {
                "name": name,
                "student_id": student_id,
                "unpaid_months": count,
            }
            for name, student_id, count in results
        ]
    }


@router.post("/{student_id}/mark-paid")
def mark_paid(
    student_id: int,
    year: int | None = None,
    month: int | None = None,
    amount: float | None = None,
    svc: StudentPaymentService = Depends(get_student_payment_service),
    user: dict = Depends(get_current_user),
):
    today = date.today()
    y = year or today.year
    m = month or today.month

    if not (1 <= m <= 12):
        raise HTTPException(status_code=400, detail="Invalid month")

    if amount is not None and amount < 0:
        raise HTTPException(status_code=400, detail="Amount cannot be negative")

    period = date(y, m, 1)

    payment = svc.mark_paid(
        student_id=student_id,
        period=period,
        amount=amount or 0.0,
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found for this student/period",
        )

    return {
        "student_id": student_id,
        "status": "paid",
        "period": period.isoformat(),
    }