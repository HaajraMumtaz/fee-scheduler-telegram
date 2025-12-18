from sqlalchemy.orm import Session
from app.db.models.student import Student
from datetime import datetime

class StudentRepository:
    def __init__(self, db: Session, user_context: dict):
        """
        db: injected SQLAlchemy session
        user_context: dictionary with user info, e.g., {'id': 1, 'branch_id': 10, 'role': 'admin'}
        """
        self.db = db
        self.user = user_context
        self.cache = {}  # simple in-memory cache

    # ------------------------
    # CREATE STUDENT
    # ------------------------
    def create(self, student: Student):
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        self._log("create", student)
        self.cache[student.id] = student  # cache the new object
        return student

    # ------------------------
    # GET BY ID
    # ------------------------
    def get_by_id(self, student_id: int):
        # first check cache
        if student_id in self.cache:
            self._log("get_by_id (cache)", self.cache[student_id])
            return self.cache[student_id]

        # fetch from DB
        student = (
            self.db.query(Student)
            .filter(Student.id == student_id)
            .filter(Student.branch_id == self.user.get("branch_id"))  # permissions
            .first()
        )
        if student:
            self.cache[student.id] = student  # cache it
        self._log("get_by_id", student)
        return student

    # ------------------------
    # GET UNPAID STUDENTS
    # ------------------------
    def get_unpaid(self):
        students = (
            self.db.query(Student)
            .filter(Student.payment_status == "unpaid")
            .filter(Student.branch_id == self.user.get("branch_id"))
            .all()
        )
        self._log("get_unpaid", f"{len(students)} students")
        return students

    # ------------------------
    # MARK AS PAID
    # ------------------------
    def mark_paid(self, student_id: int):
        student = self.get_by_id(student_id)
        if student:
            student.payment_status = "paid"
            self.db.commit()
            self._log("mark_paid", student)
        return student

    # ------------------------
    # INTERNAL LOGGING
    # ------------------------
    def _log(self, action, obj):
        print(f"[{datetime.now()}] User {self.user.get('id')} | Action: {action} | Object: {obj}")
