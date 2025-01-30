from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse
)
from app.utils.helpers import register_user, user_login
from app.auth.auth_handler import create_access_token

router = APIRouter()


@router.post(
    "/users/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse
)
def register_route(user: RegisterRequest, db: Session = Depends(get_db)):
    new_user = register_user(user.username, user.email, user.password, db)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "message": "User created successfully",
    }


@router.post("/users/login", response_model=TokenResponse)
def login_route(user: LoginRequest, db: Session = Depends(get_db)):
    user_db = user_login(user.username, user.password, db)
    token = create_access_token({"sub": user_db.username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/users/{user_id}", response_model=RegisterResponse)
def user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
