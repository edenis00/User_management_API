from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.utils.helpers import create_new_user

router = APIRouter()


@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_new_user(user.username, user.email, user.password, db)
    return {'message': 'User created successfully', 'data': new_user}


@router.get("/users/{user_id}", response_model=UserResponse)
def user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
