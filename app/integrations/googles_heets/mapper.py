def map_sheet_row_to_student_data(row: dict) -> dict:
    return {
        "name": row["name"].strip(),
        "fee_due_day": int(row["fee_due_day"]),
        "poc_name": row.get("poc_name"),
        "poc_phone": row.get("poc_phone"),
    }
