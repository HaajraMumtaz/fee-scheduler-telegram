from app.db.base import Base
from app.db.engine import engine

# 🔴 IMPORTANT: import ALL models
from app.db.models import Teacher
from app.db.models import Student
from app.db.models import TeachingAssignment
from app.db.models import PayrollRun
# import every model that exists

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✅ Database tables recreated with all columns")
