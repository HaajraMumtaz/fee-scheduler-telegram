from billing_orchestrator import BillingOrchestrator
from services import student_payment,monthly_payroll,payment_reminder
from services.sheet_sync import SheetSyncOrchestrator
from pathlib import Path
from app.integrations.googles_heets.client import GoogleSheetsClient
def create_client():
        creds_path = (
            Path(__file__).resolve().parents[2] / "app" / "keys" / "creds.json"
        )

        sheets = GoogleSheetsClient(
            credentials_path=str(creds_path),
            spreadsheet_name="fee-scheduler",
        )

        return (sheets)

def sync_all_sheets():
    orchestrator = create_client()

    try:
        result = orchestrator.run_full_sync()
        orchestrator.db.commit()
        return result
    except Exception:
        orchestrator.db.rollback()
        raise
    finally:
        orchestrator.db.close()



from datetime import date

def run_test_flow():
    # 1. Sync
    sync_all_sheets()

    # 2. Generate fees (month start)
    BillingOrchestrator.run_month_start(date(2026, 2, 1))

    # 3. Day 1 reminders
    BillingOrchestrator.run_daily_reminders(date(2026, 2, 1))

    # 4. Simulate payment
    student_payment.mark_paid(1, date(2026, 2, 1))

    # 5. Day 2 reminders
    payment_reminder.process_due_reminders(date(2026, 2, 2))

    # 6. End of month payroll
    monthly_payroll.generate_payroll_for_month(date(2026, 2, 28))