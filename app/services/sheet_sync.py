    from datetime import date
    from sqlalchemy.orm import Session
    from app.db.repositories.student_repo import StudentRepository
    from app.db.repositories.teacher_repo import TeacherRepository
    from app.db.models import Student,TeachingAssignment
    from app.integrations.googles_heets.mapper import map_sheet_row_to_student_data,map_sheet_row_to_assignment_data,map_sheet_row_to_teacher_data

    class StudentSyncService:
        def __init__(self, student_repo):
                self.student_repo = student_repo

        def sync_from_sheet(self, rows: list[dict]):
                result = {"created": 0, "updated": 0, "skipped": 0}
                print("STUDENT SYNC ROW COUNT:", len(rows))
                for row in rows:
                    data = map_sheet_row_to_student_data(row)
                
                    external_id = data.get("external_id")
                    
                    if not external_id:
                        result["skipped"] += 1
                        # print("external id:",external_id)
                        continue
                    
                    existing = self.student_repo.get_by_id(external_id)
                    print("id looking for:",external_id)
                    if existing:
                        changed = False
                        for field in ["name", "fee_due_date", "poc_name", "poc_phone"]:
                            new_value = data.get(field)
                            if new_value is not None and getattr(existing, field) != new_value:
                                setattr(existing, field, new_value)
                                changed = True

                        if changed:
                            self.student_repo.update(existing)
                            result["updated"] += 1
                        else:
                            result["skipped"] += 1
                    else:
                        student = Student(**data)
                        self.student_repo.create(student)

                        result["created"] += 1

                return result

    class AssignmentSyncService:
        def __init__(self, student_repo, teacher_repo, assignment_repo):
                self.student_repo = student_repo
                self.teacher_repo = teacher_repo
                self.assignment_repo = assignment_repo

        def sync_from_sheet(self, rows: list[dict]):
                result = {"created": 0, "updated": 0, "skipped": 0}

                for row in rows:
                    data = map_sheet_row_to_assignment_data(row)

                    assignment_id = data["assignment_id"]
                    
                    
                    student = (data["student_id"])
                    teacher = (data["teacher_id"])

                    if not student or not teacher:
                        result["skipped"] += 1
                        continue

                    existing = self.assignment_repo.get_by_id(data["assignment_id"])


                    if existing:
                        changed = False
                        for field in ["subject", "lessons_per_month", "rate_per_lesson"]:
                            if getattr(existing, field) != data.get(field):
                                setattr(existing, field, data.get(field))
                                changed = True

                        if changed:
                            self.assignment_repo.update(existing)
                            result["updated"] += 1
                        else:
                            result["skipped"] += 1
                    else:
                    assignment = TeachingAssignment(
                    external_id=assignment_id,   # now valid
                    student_id=student,
                    teacher_id=teacher,
                    subject=data["subject"],
                    lessons_per_month=data["lessons_per_month"],
                    rate_per_lesson=data["rate_per_lesson"],)

                    self.assignment_repo.create(assignment)

                    result["created"] += 1

                return result


    class TeacherSyncService:
        def __init__(self, teacher_repo):
                self.teacher_repo = teacher_repo

        def sync_from_sheet(self, rows: list[dict]):
                result = {"created": 0, "updated": 0, "skipped": 0}
                print("👩‍🏫 TEACHER SYNC ROW COUNT:", len(rows))

                for row in rows:
                    data = map_sheet_row_to_teacher_data(row)
                    teacher_id = data.get("teacher_id")
                    print(teacher_id)
                    if not teacher_id:
                        result["skipped"] += 1
                        continue

                    existing = self.teacher_repo.get_by_id(int(teacher_id))

                    if existing:
                        changed = False
                        for field in ["name", "phone", "status"]:
                            new_value = data.get(field)
                            if new_value is not None and getattr(existing, field) != new_value:
                                setattr(existing, field, new_value)
                                changed = True

                        if changed:
                            self.teacher_repo.update(existing)
                            result["updated"] += 1
                        else:
                            result["skipped"] += 1
                    else:
                        self.teacher_repo.create(**data)
                        result["created"] += 1

                return result
