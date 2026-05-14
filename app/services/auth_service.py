from app.db.repositories.user_repo import UserRepository
from app.services.password_service import (
    hash_password,
    verify_password
)
from app.services.jwt_service import create_access_token

class AuthService:

    @staticmethod
    def register(db, email, username, password):

        existing = UserRepository.get_by_email(db, email)

        if existing:
            raise Exception("User already exists")

        hashed = hash_password(password)

        user = UserRepository.create(db, {
            "email": email,
            "username": username,
            "hashed_password": hashed
        })

        return user

    @staticmethod
    def login(db, email, password):

        user = UserRepository.get_by_email(db, email)

        if not user:
            raise Exception("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise Exception("Invalid credentials")

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }