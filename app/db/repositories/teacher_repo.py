from sqlalchemy.orm import Session
from app.db.models import Teacher, Student
from datetime import datetime
from app.db.repositories.base_repo import BaseRepository

class TeacherRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, teacher_id: int):
        return self.db.query(Teacher).filter_by(id=teacher_id).first()

    def create(self, **data):
        teacher = Teacher(**data)
        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        return teacher

    def update(self, teacher: Teacher):
        self.db.add(teacher)
        self.db.commit()
        self.db.refresh(teacher)
        return teacher
