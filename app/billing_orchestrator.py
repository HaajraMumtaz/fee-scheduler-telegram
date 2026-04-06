from services.monthlyfee_gen import MonthlyFeeService
from services.monthly_payroll import PayrollService
from services.payment_reminder import PaymentReminderService
from datetime import date


class BillingOrchestrator:

    def __init__(self, db):
        self.db = db
        self.fee_service = MonthlyFeeService(db)
        self.reminder_service = PaymentReminderService(db)
        self.payroll_service = PayrollService(db)

    def run_month_start(self, date:date):
        """
        Runs on the 1st of every month
        """
        month=date.month
        return self.fee_service.generate_for_month(month)

    def run_daily_reminders(self):
        """
        Runs every day
        """
        return self.reminder_service.process_due_reminders()

    def run_payroll(self, date:date):
        """
        Runs end of month
        """
        month=date.month
        return self.payroll_service.generate_payroll_for_month(month)