
from pathlib import Path
from app.integrations.googles_heets.client import GoogleSheetsClient
from app.db.engine import SessionLocal
from app.db.repositories.student_repo import StudentRepository
from app.db.repositories.teacher_repo import TeacherRepository
from app.db.repositories.assignment_repo import TeachingAssignmentRepository
from app.services.sheet_sync import StudentSyncService, TeacherSyncService, AssignmentSyncService

def make_client() -> GoogleSheetsClient:
    """Create and return a GoogleSheetsClient instance."""
    creds_path = (
        Path(__file__).resolve().parents[2] / "app" / "keys" / "creds.json"
    )
    print(f"Using creds path: {creds_path}")

    return GoogleSheetsClient(
        credentials_path=str(creds_path),
        spreadsheet_name="fee-scheduler",
    )

def debug_dump(sheets: GoogleSheetsClient, worksheet_name: str):
    ws = sheets.sheet.worksheet(worksheet_name)
    rows = ws.get_all_values()
    print("RAW SHEET DATA:")
    for r in rows:
        print(r)


def sync_all_sheets():
    db = SessionLocal()
    sheets = make_client()

    # -------------------
    # STUDENTS
    # -------------------
    student_rows = sheets.get_students("Students")
    print("STUDENT SYNC ROW COUNT:", len(student_rows))
    student_repo = StudentRepository(db)
    student_service = StudentSyncService(student_repo)
    student_result = student_service.sync_from_sheet(student_rows)
    print("📄 Students Sync Result:", student_result)

    # -------------------
    # TEACHERS
    # -------------------
    teacher_rows = sheets.get_teachers("Teachers")
    teacher_repo = TeacherRepository(db)
    teacher_service = TeacherSyncService(teacher_repo)
    teacher_result = teacher_service.sync_from_sheet(teacher_rows)
    print("👩‍🏫 Teachers Sync Result:", teacher_result)

    # -------------------
    # ASSIGNMENTS
    # -------------------
    assignment_rows = sheets.get_assignments("Assignments")
    assignment_repo = TeachingAssignmentRepository(db)
    assignment_service = AssignmentSyncService(student_repo, teacher_repo, assignment_repo)
    assignment_result = assignment_service.sync_from_sheet(assignment_rows)
    print("📚 Assignments Sync Result:", assignment_result)

    db.close()


if __name__ == "__main__":
    sheets = make_client()
    sync_all_sheets()
    


