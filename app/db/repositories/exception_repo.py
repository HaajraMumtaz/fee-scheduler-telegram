from sqlalchemy.orm import Session
from datetime import date
from app.db.models import TeachingException, TeachingAssignment


class TeachingExceptionRepository:
    def __init__(self, db: Session):
        """
        db: SQLAlchemy session
        """
        self.db = db

    # ---------------------------------
    # CREATE EXCEPTION
    # ---------------------------------
    def create(
        self,
        assignment_id: int,
        exception_date: date,
        lessons_missed: int = 1,
        reason: str | None = None
    ):
        """
        Records a teaching exception.
        Example:
        - teacher missed 1 lesson on Jan 10
        """

        exception = TeachingException(
            assignment_id=assignment_id,
            date=exception_date,
            lessons_missed=lessons_missed,
            reason=reason
        )

        self.db.add(exception)
        self.db.commit()
        self.db.refresh(exception)

        return exception

    # ---------------------------------
    # GET EXCEPTIONS FOR ASSIGNMENT
    # ---------------------------------
    def get_by_assignment(self, assignment_id: int):
        """
        Returns all exceptions for a given teaching assignment.
        Used during payroll calculation.
        """
        return (
            self.db.query(TeachingException)
            .filter(TeachingException.assignment_id == assignment_id)
            .all()
        )

    # ---------------------------------
    # GET EXCEPTIONS FOR TEACHER (MONTH)
    # ---------------------------------
    def get_for_teacher_month(self, teacher_id: int, month: str):
        """
        Returns all exceptions for a teacher in a given month.
        month format: 'YYYY-MM'
        """

        return (
            self.db.query(TeachingException)
            .join(TeachingAssignment)
            .filter(TeachingAssignment.teacher_id == teacher_id)
            .filter(TeachingException.date.like(f"{month}%"))
            .all()
        )
