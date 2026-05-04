from fastapi import HTTPException
from app.schemas import OperationRequest
from app.api.repository import wallets as wallets_repository
from sqlalchemy.orm import Session
from app.models import User




# пополнение кошелька
def add_income(db: Session, current_user: User, operation: OperationRequest):

    # проверить существует ли такой кошелек

        if not wallets_repository.is_wallet_exists(db, current_user.id,  operation.wallet_name):
            raise HTTPException(status_code=404, detail=f"кошелька {operation.wallet_name} не cуществует")


        # добавить сумму пополнения к кошельку

        wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)

        # вернуть информацию об операции
        db.commit()
        return {
            'massage': 'пополнение выполнено успешно',
            "wallet_name": operation.wallet_name,
            "amount": operation.amount,
            'balance': wallet.balance,
            'destination': operation.destination
        }





#расход по кошельку
def add_expense(db: Session, current_user: User, operation: OperationRequest):

        # проверяем существует ли кошелек
        if not wallets_repository.is_wallet_exists(db, current_user.id, operation.wallet_name):
            raise HTTPException(status_code=404, detail=f"кошелек {operation.wallet_name} не существует")



        # проверяем достаточно ли денег на кошельке для вывода
        wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, operation.wallet_name)
        if wallet.balance < operation.amount:
            raise HTTPException(status_code=400, detail=f'сумма вывода превышает ваш баланс, баланс: {wallet.balance} сумма вывода {operation.amount}')


        # производим вывод

        wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
        db.commit()
        # выводим информацию об операции
        return {
            'massage': 'Вывод средств выполнен успешно',
            "wallet_name": operation.wallet_name,
            "amount": operation.amount,
            'balance': wallet.balance,
            'destination': operation.destination
        }
