from fastapi import APIRouter, Depends

from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return {"user": user}