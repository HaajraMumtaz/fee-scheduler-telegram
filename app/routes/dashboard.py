from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    return {"page": "dashboard UI"}  # later replace with HTML template