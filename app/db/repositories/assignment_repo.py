from sqlalchemy.orm import Session
from app.db.models import TeachingAssignment, TeachingException
from sqlalchemy import func
from datetime import date

class TeachingAssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------
    # CREATE ASSIGNMENT
    # ------------------------
    def create(self, assignment: TeachingAssignment):
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    def update(self, assignment: TeachingAssignment):
        self.db.add(assignment)   # safe even if already attached
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    # ------------------------
    # GET BY ID
    # ------------------------
    def get_by_id(self, assignment_id: int):
        return (
            self.db.query(TeachingAssignment)
            .filter(TeachingAssignment.id == assignment_id)
            .first()
        )

    # ------------------------
    # GET ASSIGNMENTS FOR A STUDENT
    # ------------------------
    def get_by_student(self, student_id: int):
        return (
            self.db.query(TeachingAssignment)
            .filter(TeachingAssignment.student_id == student_id)
            .all()
        )

    # ------------------------
    # GET ASSIGNMENTS FOR A TEACHER
    # ------------------------
    def get_by_teacher(self, teacher_id: int):
        return (
            self.db.query(TeachingAssignment)
            .filter(TeachingAssignment.teacher_id == teacher_id)
            .all()
        )

    # ------------------------
    # CALCULATE PAYABLE LESSONS (MONTH)
    # ------------------------
    def payable_lessons(self, assignment_id: int, month: str):
        """
        month: 'YYYY-MM'
        """
        assignment = self.get_by_id(assignment_id)
        if not assignment:
            return 0

        missed = (
            self.db.query(func.coalesce(func.sum(TeachingException.lessons_missed), 0))
            .filter(TeachingException.assignment_id == assignment_id)
            .filter(func.strftime("%Y-%m", TeachingException.date) == month)
            .scalar()
        )

        return max(assignment.lessons_per_month - missed, 0)
    
    def get_by_external_id(self, external_id: int):
        return (
            self.db.query(TeachingAssignment)
            .filter(TeachingAssignment.external_id == external_id)
            .first()
        )

