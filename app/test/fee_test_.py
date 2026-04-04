from datetime import date
from app.db.engine import SessionLocal
from app.db.models import Student, TeachingAssignment, MonthlyFee
from app.services.monthlyfee_gen import MonthlyFeeService

def test_monthly_fee_generation(month: str):
    db = SessionLocal()
    
    service = MonthlyFeeService(db)
    
    
    result = service.generate_for_month(month)
    print("Monthly Fee Generation Result:", result)
    
    # Verify fees created in DB
    fees = db.query(MonthlyFee).filter(MonthlyFee.month == month).all()
    for f in fees:
        print(f"Student ID: {f.student_id}, Amount: {f.amount}, Due: {f.due_date}, Status: {f.status}")
    
    db.close()

# Run test for February 2026
test_monthly_fee_generation("2026-02")
