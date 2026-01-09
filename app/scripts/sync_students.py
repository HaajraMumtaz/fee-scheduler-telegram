from app.db.session import SessionLocal
from app.integrations.google_sheets.client import GoogleSheetsClient
from app.repositories.student_repository import StudentRepository
from app.services.student_sync_service import StudentSyncService

def run():
    db = SessionLocal()

    sheets = GoogleSheetsClient(
        creds_path="creds.json",
        sheet_name="Fee Scheduler"
    )

    rows = sheets.get_students()

    student_repo = StudentRepository(db)
    service = StudentSyncService(student_repo)

    result = service.sync_from_sheet(rows)
    print("SYNC RESULT:", result)

if __name__ == "__main__":
    run()
