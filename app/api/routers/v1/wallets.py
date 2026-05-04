from fastapi import APIRouter, Depends
from app.api.services import wallets as wallets_service
from app.schemas import CreateWalletRequest
from app.dependency import get_db, get_current_user
from sqlalchemy.orm import Session
from app.models import User

router = APIRouter()




#ручка для получения баланса кошелька или общего
@router.get('/balance')
def get_balance(wallet_name: str | None = None, current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):

    return wallets_service.get_balance(db, current_user, wallet_name)



#создать кошелек с балансом 0 и пополнить его
@router.post('/wallets')
def create_wallet(wallet: CreateWalletRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

   return wallets_service.create_wallet(db, current_user, wallet)



# Эндпоинт для получения списка всех кошельков пользователя
@router.get('/wallets_list')
def get_wallets_list(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Используем уже готовый метод из репозитория
    return wallets_service.wallets_repository.get_all_wallets(db, current_user.id)