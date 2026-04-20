from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.get("/login")
def login_page():
    return {"page": "login UI here"}  # replace with template later


@router.post("/login")
def login():
    # TODO: validate user
    return {"message": "logged in"}


@router.post("/logout")
def logout():
    return {"message": "logged out"}


@router.get("/me")
def me():
    return {"user": "current_user"}