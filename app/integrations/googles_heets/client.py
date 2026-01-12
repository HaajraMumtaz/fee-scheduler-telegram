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
        students = []

        for row in raw_rows:
            try:
                students.append({
                    "name": row.get("Student Name", "").strip(),
                    "poc_name": row.get("POC Name", "").strip(),
                    "poc_phone": str(row.get("POC Phone", "")).strip(),
                    "fee_due_day": int(row.get("Fee Due Day")),
                })
            except (TypeError, ValueError):
                # skip malformed rows safely
                continue

        return students
