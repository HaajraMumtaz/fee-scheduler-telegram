from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService.register(
            db=db,
            email=body.email,
            username=body.username,
            password=body.password,
        )
        return {"id": user.id, "email": user.email, "username": user.username}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        result = AuthService.login(db=db, email=body.email, password=body.password)

        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            httponly=True,        # JS cannot read it
            samesite="lax",
            secure=True,          # HTTPS only — set False for local dev
            max_age=60 * 60,      # 1 hour, match ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return {"message": "Logged in successfully."}

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=True,
    )
    return {"message": "Logged out successfully."}


@router.get("/me")
def me(request: Request):
    # lightweight check without hitting DB — just validates the token
    from services.jwt_service import decode_access_token
    from jose import JWTError, ExpiredSignatureError

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        return {"user_id": payload.get("sub"), "email": payload.get("email")}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")