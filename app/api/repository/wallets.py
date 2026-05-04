from decimal import Decimal

from app.database import SessionLocal
from app.schemas import CreateWalletRequest
from app.models import Wallet
from sqlalchemy.orm import Session
from app.models import User


# проверка на то, существует ли кошелек
def is_wallet_exists(db: Session, user_id: int, wallet_name: str) -> bool:


        return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first() is not None


# пополняет баланс кошелька
def add_income(db: Session, user_id: int,  wallet_name: str, amount: Decimal) -> Wallet:



    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balance += Decimal(amount)
    return wallet


# вывод денег из кошелька
def add_expense(db: Session, user_id: int,  wallet_name: str, amount: Decimal) -> Wallet:

        wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
        wallet.balance -= Decimal(amount)
        return wallet

#поиск кошелька по его названию
def get_wallet_balance_by_name(db: Session, user_id: int,  wallet_name: str) -> Wallet:

        return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()



# вернуть сумму всех кошельков
def get_all_wallets(db: Session, user_id: int, wallet_name=None)-> list[Wallet]:

    return db.query(Wallet).filter(User.id == user_id, Wallet.user_id == user_id).all()



# создание кошелька
def create_wallet(db: Session, user_id: int, wallet_name: str, amount: float) -> Wallet:

        wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id)
        db.add(wallet)
        db.flush()
        return wallet

