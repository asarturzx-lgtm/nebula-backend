from fastapi import HTTPException

from app.database import SessionLocal
from app.schemas import CreateWalletRequest
from app.api.repository import wallets as wallets_repository
from sqlalchemy.orm import Session
from app.models import User



#получение баланса кошелька или общего баланса
def get_balance(db: Session, current_user: User, wallet_name: str | None = None):

        # Если имя кошелька не указано возвращаем общий баланс
        if wallet_name is None:
            wallets = wallets_repository.get_all_wallets(db,current_user.id, wallet_name)
            return {"balance": sum([w.balance for w in wallets])}

        #Если такой кошелек уже есть вернем ошибку
        if not wallets_repository.is_wallet_exists(db, current_user.id,   wallet_name):
            raise HTTPException(status_code=404, detail="Такого кошелька нет")

        #Возвращаем баланс конкретного кошелька
        wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id,   wallet_name)
        db.commit()
        return {
            'massage': f'кошелек: {wallet.name}',
            'balance': wallet.balance
        }

#создать кошелек с балансом 0 и пополнить его
def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest):

        #Проверяем не существует ли такой кошелек
        if wallets_repository.is_wallet_exists(db, current_user.id,    wallet.name):
            raise HTTPException(status_code=400, detail="Такой кошелек уже создан")

        #Создаем новый кошелек с начальным балансом
        wallet = wallets_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance)

        #Возвращаем информацию о созданном кошельке
        db.commit()
        return {
            'massage': f'кошелек {wallet.name} создан',
            'balance': wallet.balance,

        }
