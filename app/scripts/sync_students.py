from app.db.engine import SessionLocal
from app.integrations.googles_heets.client import GoogleSheetsClient
from app.db.repositories.student_repo import StudentRepository
from app.services.sheet_sync import StudentSyncService

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
