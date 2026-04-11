
from datetime import date
from app.db.models import MonthlyFee, PaymentState
from app.services.student_payment import StudentPaymentService
from sqlalchemy import func, or_


class PaymentReminderService:

    def __init__(self, db, student_payment_service:StudentPaymentService):
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

        for student_name,student_id,unpaid_months in results:
            message = {
                "student_name": student_name,
                "text": f"{student_name} - {unpaid_months} months due"
            }
            formatted_list.append(message)
        print("All reminders created for today!\n",formatted_list)
        return formatted_list
    import requests

def send_telegram_reminder(bot_token, chat_id, student_name, fee_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": f"Reminder: Fee for {student_name} is due!",
        "reply_markup": {
            "inline_keyboard": [[
                {
                    "text": "✅ Mark as Paid",
                    "callback_data": f"pay:{fee_id}"  # This is the 'pay:fee_id'
                }
            ]]
        }
    }
    requests.post(url, json=payload)