
from datetime import date
from app.db.models import MonthlyFee, PaymentState
from sqlalchemy import func, or_


class PaymentReminderService:

    def __init__(self, db, student_payment_service):
        self.db = db
        self.student_payment_service = student_payment_service

    def process_due_reminders(self):
        """
        Daily job:
        - fetch unpaid students
        - format for Telegram
        """

        # 1️⃣ Get unpaid students (single source of truth)
        results = self.student_payment_service.get_unpaid_students()

        # 2️⃣ Format for Telegram
        formatted_list = []

        for student_id, student_name,unpaid_months in results:
            message = {
                "student_name": student_name,
                "text": f"{student_name} - {unpaid_months} months due"
            }
            formatted_list.append(message)
        print("All reminders created for today!\n",formatted_list)
        return formatted_list