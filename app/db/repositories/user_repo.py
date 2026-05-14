from app.db.models import User

class UserRepository:

    @staticmethod
    def get_by_email(db, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db, user_data):
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user