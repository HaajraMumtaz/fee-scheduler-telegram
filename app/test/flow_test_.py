
from app.services.student_payment import StudentPaymentService
from app.services.monthly_payroll import PayrollService
from app.services.payment_reminder import PaymentReminderService
from app.billing_orchestrator import BillingOrchestrator
from app.services.sheet_sync import SheetSyncOrchestrator
from pathlib import Path
from app.db.models import MonthlyFee
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
    # sync_all_sheets(db)
    # print("synced")
    billingObj=BillingOrchestrator(db)
    studentObj=StudentPaymentService(db)

  
    billingObj.run_month_start(date(2026, 4, 1))
    # debug_view_table(db, MonthlyFee)
    billingObj.run_daily_reminders()

    studentObj.mark_paid(3, date(2026, 3, 7))
    billingObj.run_daily_reminders()
    
    # debug_view_table(db, MonthlyFee)
    # print("------")
    # studentObj.mark_paid(5, date(2026, 3, 7))
    # debug_view_table(db, MonthlyFee)
    # billingObj.run_daily_reminders()
    # print("------")
    # 6. End of month payroll
    billingObj.run_payroll(date(2026, 4, 28))

    db.close()




import json
from sqlalchemy import select

def debug_view_table(session, model_class):
    """
    Standalone function to dump all rows of a table to the console.
    """
    # 1. Select all records
    records = session.query(model_class).all()
    
    # 2. Convert each row to a dictionary
    table_data = []
    for row in records:
        # Professional trick: iterate through columns defined in the model
        row_dict = {
            col.name: getattr(row, col.name) 
            for col in row.__table__.columns
        }
        table_data.append(row_dict)
    
    # 3. Print as formatted JSON
    print(f"\n--- DATA DUMP: {model_class.__tablename__.upper()} ---")
    if not table_data:
        print("Empty table.")
    else:
        # default=str handles dates and enums that JSON normally can't read
        print(json.dumps(table_data, indent=4, default=str))
    print("---------------------------------\n")


run_test_flow()
