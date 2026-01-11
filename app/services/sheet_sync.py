
from datetime import date
from sqlalchemy.orm import Session
from db.repositories.student_repo import StudentRepository

from app.integrations.googles_heets.mapper import map_sheet_row_to_student_data

class StudentSyncService:
    def __init__(self, student_repo):
        self.student_repo = student_repo

    def sync_from_sheet(self, rows: list[dict]):
        result = {
            "created": 0,
            "updated": 0,
            "skipped": 0
        }

        for row in rows:
            data = map_sheet_row_to_student_data(row)

            existing = self.student_repo.get_by_name(data["name"])

            if existing:
                changed = False

                for field in ["fee_due_day", "poc_name", "poc_phone"]:
                    if getattr(existing, field) != data[field]:
                        setattr(existing, field, data[field])
                        changed = True

                if changed:
                    self.student_repo.update(existing)
                    result["updated"] += 1
                else:
                    result["skipped"] += 1
            else:
                self.student_repo.create(**data)
                result["created"] += 1

        return result
