
from app.services.student_payment import StudentPaymentService
from app.services.monthly_payroll import PayrollService
from app.services.payment_reminder import PaymentReminderService
from app.billing_orchestrator import BillingOrchestrator
from app.services.sheet_sync import SheetSyncOrchestrator
from pathlib import Path
from app.integrations.googles_heets.client import GoogleSheetsClient
from app.db.engine import SessionLocal
def create_client():
        creds_path = (
            Path(__file__).resolve().parents[2] / "app" / "keys" / "creds.json"
        )

        sheets = GoogleSheetsClient(
            credentials_path=str(creds_path),
            spreadsheet_name="fee-scheduler",
        )

        return (sheets)

def sync_all_sheets(db):
    sheets = create_client()
    orchestrator = SheetSyncOrchestrator(db, sheets)
    try:
        result = orchestrator.run_full_sync()
        orchestrator.db.commit()
        return result
    except Exception:
        orchestrator.db.rollback()
        print("failed sync")
        raise




from datetime import date

def run_test_flow():
    
    db=SessionLocal()
    # 1. Sync
    sync_all_sheets(db)
    print("synced")
    billingObj=BillingOrchestrator(db)
    studentObj=StudentPaymentService(db)

    # 2. Generate fees (month start)
    billingObj.run_month_start(date(2026, 2, 1))

    # 3. Day 1 reminders
    billingObj.run_daily_reminders()

    # 4. Simulate payment
    studentObj.mark_paid(1, date(2026, 2, 1))

    # 5. Day 2 reminders
    billingObj.run_daily_reminders()

    # 6. End of month payroll
    billingObj.run_payroll(date(2026, 2, 28))

    db.close()

run_test_flow()