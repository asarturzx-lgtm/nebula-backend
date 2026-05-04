from app.api.services import operations as operations_service
from app.schemas import OperationRequest
from fastapi import APIRouter, Depends
from app.dependency import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.dependency import get_current_user

router = APIRouter()

# пополнение кошелька
@router.post('/operations/income')
def add_income(operation: OperationRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return operations_service.add_income(db, current_user, operation)



#расход по кошельку
@router.post('/operations/expense')
def add_expense(operation: OperationRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return operations_service.add_expense(db, current_user, operation)


