def map_sheet_row_to_student_data(row: dict) -> dict:
    try:
       
        
        return {
            "external_id": row["student_id"],
            "name": row["name"].strip(),
            "fee_due_day": int(row["fee_due_day"]),
            "poc_name": row.get("poc_name") or None,
            "poc_phone": row.get("poc_phone") or None,
        }
    except Exception as e:
        import traceback
        traceback.print_exc() # This shows the exact line number that failed
        return {}
def map_sheet_row_to_assignment_data(row: dict) -> dict:
    required = ["assignment_id", "student_id", "teacher_id"]

    if not all(row.get(k) for k in required):
        print("❌ Missing required IDs:", row)
        return {}

    try:
        return {
            "assignment_id": int(str(row["assignment_id"]).strip()),
            "student_id": int(str(row["student_id"]).strip()),
            "teacher_id": int(str(row["teacher_id"]).strip()),
            "subject": str(row.get("subject", "")).strip(),
            "lessons_per_month": int(row.get("lessons_per_month", 0)),
            "rate_per_lesson": float(row.get("rate_per_lesson", 0)),
        }
    except ValueError as e:
        print("❌ Invalid numeric value:", e, row)
        return {}

def map_sheet_row_to_teacher_data(row: dict) -> dict:
    if not row.get("teacher_id"):
        print("❌ Missing teacher_id:", row)
        return {}

    try:
    
        return {
            "teacher_id": int(str(row["teacher_id"]).strip()),
            "name": str(row.get("teacher_name", "")).strip(),
            "phone": str(row["phone"]).strip() if row.get("phone") else None,
            "status": row.get("status", "active"),
        }
        
    except ValueError as e:
        print("❌ Invalid teacher row:", e, row)
        return {}

   
