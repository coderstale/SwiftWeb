from sqlalchemy.orm import Session
from passlib.context import CryptContext
from my_framework.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, email: str, password: str, role: str):
    hashed_password = pwd_context.hash(password)
    user = User(
        username=username, email=email, hashed_password=hashed_password, role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
