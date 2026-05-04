from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.api.repository import users as repository_users

from app.database import SessionLocal

security = HTTPBearer()
# генератор сессий
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# зависимость авторизации
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)):
    login = credentials.credentials

    user = repository_users.get_user(db, login)

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user