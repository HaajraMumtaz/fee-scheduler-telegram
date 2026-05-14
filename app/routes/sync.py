from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.billing_orchestrator import BillingOrchestrator
from app.integrations.googles_heets.client import GoogleSheetsClient
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/sync", tags=["Sync"])


def get_orchestrator(db: Session = Depends(get_db)) -> BillingOrchestrator:
    return BillingOrchestrator(db)


@router.post("/sheets")
def sync_sheets(
    orchestrator: BillingOrchestrator = Depends(get_orchestrator),
    user: dict = Depends(get_current_user),
):
    sheets = GoogleSheetsClient()
    return orchestrator.run_sheet_sync(sheets)