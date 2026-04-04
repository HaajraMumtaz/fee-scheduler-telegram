from app.db.engine import SessionLocal
from app.db.models import Student, Teacher, TeachingAssignment, MonthlyFee

db = SessionLocal()

print("=== Students ===")
for s in db.query(Student).all():
    print(vars(s))

print("\n=== Teachers ===")
for t in db.query(Teacher).all():
    print(vars(t))

print("\n=== Assignments ===")
for a in db.query(TeachingAssignment).all():
    print(vars(a))

print("\n=== Monthly Fees ===")
for m in db.query(MonthlyFee).all():
    print(vars(m))

db.close()
