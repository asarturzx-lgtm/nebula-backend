from sqlalchemy.orm import Session
from app.api.repository import users as users_repository
from app.schemas import UserResponse
from fastapi import HTTPException


def create_user(db: Session, login: str):
    if users_repository.get_user(db, login):
        raise HTTPException(status_code=400, detail="Такой пользователь уже есть")


    user = users_repository.create_user(db, login)
    db.commit()
    return UserResponse.model_validate(user)