from fastapi import APIRouter
from app.billing_orchestrator import BillingOrchestrator

router = APIRouter(prefix="/api/students")

# assume injected later via dependency or global
orchestrator = None


@router.get("/unpaid")
def get_unpaid_students():
    return {"students": []}


@router.post("/{student_id}/mark-paid")
def mark_paid(student_id: int):
    # this is your popup confirmation final action
    return {
        "student_id": student_id,
        "status": "paid"
    }