from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.services.payment_reminder import PaymentReminderService
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/reminders", tags=["Reminders"])


def get_reminder_service(db: Session = Depends(get_db)) -> PaymentReminderService:
    return PaymentReminderService(db, None)


@router.get("/")
def get_all_reminders(
    svc: PaymentReminderService = Depends(get_reminder_service),
    user: dict = Depends(get_current_user),
):
    reminders = svc.process_due_reminders()
    return {"count": len(reminders), "data": reminders}


@router.get("/{student_id}")
def get_student_reminders(
    student_id: int,
    svc: PaymentReminderService = Depends(get_reminder_service),
    user: dict = Depends(get_current_user),
):
    # filter from all reminders — replace with a targeted service
    # method if PaymentReminderService supports it later
    reminders = svc.process_due_reminders()
    student_reminders = [r for r in reminders if r.get("student_id") == student_id]

    if not student_reminders:
        raise HTTPException(status_code=404, detail="No reminders found for this student")

    return {
        "student_id": student_id,
        "count": len(student_reminders),
        "data": student_reminders,
    }