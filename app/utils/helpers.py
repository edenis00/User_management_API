from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


def create_new_user(username: str, email: str, password: str, db: Session):
    if get_user_by_email(email, db):
        raise HTTPException(status_code=400, detail="Email already exists")

    if get_user_by_username(username, db):
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
