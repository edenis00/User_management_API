from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def check_user_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def check_user_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


def register_user(username: str, email: str, password: str, db: Session):
    if check_user_email(email, db):
        raise HTTPException(status_code=400, detail="Email already exists")

    if check_user_username(username, db):
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(password)

    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def user_login(username: str, password: str, db: Session):
    user_db = check_user_username(username, db)

    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(password, user_db.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return user_db
