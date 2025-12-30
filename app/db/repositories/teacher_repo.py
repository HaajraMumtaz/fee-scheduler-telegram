from sqlalchemy.orm import Session
from app.db.models import Teacher, Student, Transaction
from datetime import datetime


class TeacherRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, teacher: Teacher):
        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        return teacher

    def get_by_id(self, teacher_id: int):
        return self.db.query(Teacher).filter_by(id=teacher_id).first()

    def list_all(self):
        return self.db.query(Teacher).all()
