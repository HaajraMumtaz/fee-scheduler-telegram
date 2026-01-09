# app/integrations/sheets_client.py

import gspread
from google.oauth2.service_account import Credentials


class GoogleSheetsClient:
    def __init__(self, credentials_path: str, spreadsheet_name: str):
        self.credentials_path = credentials_path
        self.spreadsheet_name = spreadsheet_name
        self.client = self._authenticate()

    def _authenticate(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ]

        creds = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=scopes
        )

        return gspread.authorize(creds)

    def get_students(self, worksheet_name: str):
        """
        Returns list of dicts:
        [
            {
              'student_name': str,
              'poc_name': str,
              'poc_phone': str,
              'fee_due_day': int
            }
        ]
        """
        sheet = self.client.open(self.spreadsheet_name)
        worksheet = sheet.worksheet(worksheet_name)

        rows = worksheet.get_all_records()

        students = []
        for row in rows:
            students.append({
                "student_name": row.get("Student Name"),
                "poc_name": row.get("POC Name"),
                "poc_phone": row.get("POC Phone"),
                "fee_due_day": int(row.get("Fee Due Day"))
            })

        return students
