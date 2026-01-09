from sqlalchemy.orm import Session
from app.db.models import Student,PaymentState
from datetime import datetime

class StudentRepository:
    def __init__(self, db: Session):
        """
        db: SQLAlchemy session (unit of work)
        user_context: who is performing the action
        """
        self.db = db


    # ------------------------
    # CREATE STUDENT
    # ------------------------
    def create(self, student: Student):
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    

    # ------------------------
    # GET BY ID
    # ------------------------
    def get_by_id(self, student_id: int):
        return (
            self.db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )


        # fetch from DB
    def get_unpaid_students(self):
        return (
            self.db.query(Student)
            .filter(Student.payment_state != PaymentState.paid)
            .all()
        )


  
        return student

    def mark_paid(self, student_id: int):
        student = self.get_by_id(student_id)
        if not student:
            return None

        student.payment_state = PaymentState.paid
        self.db.commit()
        return student

    # ------------------------
    # INTERNAL LOGGING
    # ------------------------
    def _log(self, action, obj):
        print(f"[{datetime.now()}] User {self.user.get('id')} | Action: {action} | Object: {obj}")
