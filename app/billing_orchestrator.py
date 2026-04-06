from app.services.monthlyfee_gen import MonthlyFeeService
from app.services.monthly_payroll import PayrollService
from app.services.payment_reminder import PaymentReminderService
from app.services.student_payment import StudentPaymentService
from datetime import date


class BillingOrchestrator:

    def __init__(self, db):
        self.db = db
        self.fee_service = MonthlyFeeService(db)
        self.student_service=StudentPaymentService(db)
        self.reminder_service = PaymentReminderService(db=db, 
        student_payment_service=self.student_service)
        self.payroll_service=PayrollService(db)
        self.fee_service=MonthlyFeeService(db)

    def run_month_start(self, date:date):
        """
        Runs on the 1st of every month
        """
        
        return self.fee_service.generate_for_month(date)

    def run_daily_reminders(self):
        """
        Runs every day
        """
        return self.reminder_service.process_due_reminders()

    def run_payroll(self, date:date):
        """
        Runs end of month
        """
        
        return self.payroll_service.generate_payroll_for_month(date)