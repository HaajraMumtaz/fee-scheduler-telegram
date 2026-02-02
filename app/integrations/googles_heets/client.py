# app/integrations/sheets_client.py

import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict


class GoogleSheetsClient:
    def __init__(self, credentials_path: str, spreadsheet_name: str):
        self.credentials_path = credentials_path
        self.spreadsheet_name = spreadsheet_name
        self.client = self._authenticate()
        self.sheet = self.client.open(self.spreadsheet_name)

    def _authenticate(self):
            
            SCOPES = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=SCOPES
            )
            return gspread.authorize(creds)

    # ----------------------------
    # GENERIC WORKSHEET READER
    # ----------------------------
    def get_rows(self, worksheet_name: str) -> List[Dict]:
        """
        Returns raw rows as dictionaries using header row.
        Example:
        [
            {"Student Name": "Ali", "Fee Due Day": "5", ...}
        ]
        """
        worksheet = self.sheet.worksheet(worksheet_name)
        return worksheet.get_all_records()

    # ----------------------------
    # STUDENT-SPECIFIC HELPER
    # ----------------------------
    def get_students(self, worksheet_name: str) -> List[Dict]:
        """
        Returns normalized student rows.
        DOES NOT touch DB.
        DOES NOT return ORM objects.
        """

        raw_rows = self.get_rows(worksheet_name)

        normalized_rows = []
        for row in raw_rows:
            normalized_rows.append({
                k.strip().lower().replace(" ", "_"): v
                for k, v in row.items()
            })

        return normalized_rows
 # ----------------------------
    # TEACHER-SPECIFIC HELPER
    # ----------------------------
    def get_teachers(self, worksheet_name: str) -> list[dict]:
        """
        Returns normalized student rows.
        DOES NOT touch DB.
        DOES NOT return ORM objects.
        """
        raw_rows = self.get_rows(worksheet_name)

        normalized_rows = []
        for row in raw_rows:
            normalized_rows.append({
                k.strip().lower().replace(" ", "_"): v
                for k, v in row.items()
            })

        return normalized_rows


    # ----------------------------
    # ASSIGNMENT-SPECIFIC HELPER
    # ----------------------------
    def get_assignments(self, worksheet_name: str) -> list[dict]:
        raw_rows = self.get_rows(worksheet_name)
        assignments = []

        for row in raw_rows:
            try:
                assignments.append({
                    "assignment_id": row.get("assignment_id"),
                    "student_id": row.get("student_id"),
                    "teacher_id": row.get("teacher_id"),

                    # keep names for readability/debugging
                    "student_name": row.get("Student Name", "").strip(),
                    "teacher_name": row.get("Teacher Name", "").strip(),

                    "subject": row.get("Subject", "").strip(),
                    "lessons_per_month": int(row.get("Lessons/Month", 0)),
                    "rate_per_lesson": float(row.get("Rate/Lesson", 0)),
                })
            except (TypeError, ValueError):
                continue

        return assignments
