from pathlib import Path
from app.integrations.googles_heets.client import GoogleSheetsClient


def make_client() -> GoogleSheetsClient:
    """Create and return a GoogleSheetsClient instance."""
    creds_path = (
        Path(__file__).resolve().parents[2]
        / "app"
        / "keys"
        / "creds.json"
    )

    print(f"Using creds path: {creds_path}")

    return GoogleSheetsClient(
        credentials_path=str(creds_path),
        spreadsheet_name="fee-scheduler",
    )


def main():
    sheets = make_client()

    ws = sheets.sheet.worksheet("Students")
    students = ws.get_all_values()

    print("\n📄 STUDENTS FROM SHEET:\n")
    for row in students:
        print(row)

    print(f"\n✅ Total rows read: {len(students)}")


def debug_dump(worksheet_name: str):
    sheets = make_client()

    ws = sheets.sheet.worksheet(worksheet_name)
    rows = ws.get_all_values()

    print(f"\n🧪 RAW SHEET DATA ({worksheet_name}):\n")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
    # main()
