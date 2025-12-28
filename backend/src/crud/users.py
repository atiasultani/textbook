from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime

from src.models.users import User as UserDB
from src.auth.schemas import UserCreate, UserUpdate, UserResponse
from src.auth.security import get_password_hash

# -------------------------
# User CRUD
# -------------------------

def get_user_by_id(db: Session, user_id: str) -> Optional[UserResponse]:
    user_db = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user_db:
        return UserResponse.from_orm(user_db)
    return None

def get_user_by_email(db: Session, email: str) -> Optional[UserResponse]:
    user_db = db.query(UserDB).filter(UserDB.email == email).first()
    if user_db:
        return UserResponse.from_orm(user_db)
    return None

def create_user(db: Session, user: UserCreate) -> UserResponse:
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserResponse.from_orm(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
