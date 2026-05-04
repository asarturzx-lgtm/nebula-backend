from sqlalchemy.orm import Session
from app.models import User



#Запрос для проверки существует ли юзер
def get_user(db: Session, login: str):
    return db.query(User).filter(User.login == login).scalar()

# Запрос для создания юзера
def create_user(db: Session, login: str) -> User:
    user = User(login=login)
    db.add(user)
    db.flush()
    return user

