from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.models import Teacher
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/teachers", tags=["Teachers"])


def get_teacher_or_404(db: Session, teacher_id: int) -> Teacher:
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.get("/")
def list_teachers(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return {
        "teachers": [
            {
                "id": t.id,
                "teacher_id": t.teacher_id,
                "name": t.name,
                "phone": t.phone,
                "status": t.status,
            }
            for t in db.query(Teacher).all()
        ]
    }


@router.get("/{teacher_id}")
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    teacher = get_teacher_or_404(db, teacher_id)

    return {
        "id": teacher.id,
        "teacher_id": teacher.teacher_id,
        "name": teacher.name,
        "phone": teacher.phone,
        "status": teacher.status,
        "assignments": [
            {
                "id": a.id,
                "subject": a.subject,
                "lessons_per_month": a.lessons_per_month,
                "rate_per_lesson": a.rate_per_lesson,
                "active": a.active,
            }
            for a in teacher.assignments
        ],
    }


@router.patch("/{teacher_id}/deactivate")
def deactivate_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    teacher = get_teacher_or_404(db, teacher_id)
    teacher.status = "inactive"
    db.commit()

    return {"teacher_id": teacher_id, "status": "inactive"}