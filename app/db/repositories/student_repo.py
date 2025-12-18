from sqlalchemy.orm import Session
from app.db.models import Student

class StudentRepository:
    @staticmethod
    def create(db: Session, student: Student):
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def get_by_id(db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()

    @staticmethod
    def get_unpaid(db: Session):
        return db.query(Student).filter(
            Student.payment_status == "unpaid"
        ).all()

    @staticmethod
    def mark_paid(db: Session, student_id: int):
        student = db.query(Student).get(student_id)
        if student:
            student.payment_status = "paid"
            db.commit()
        return student
