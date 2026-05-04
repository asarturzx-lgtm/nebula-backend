from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

# класс пополнения и вывода
class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=30)
    amount: Decimal
    destination: str | None = Field(None, max_length=120)



    # Проверка пополениея/вывода на отрицательное значение
    @field_validator('amount')
    def validate_amount_positive(cls, value: Decimal) -> Decimal:
        #Проверка на отрицательное значение
        if value <= 0:
            raise ValueError('Сумма должна быть положительной')
        #Возвращаем value
        return value


    @field_validator('wallet_name')
    def validate_wallet_name_not_empty(cls, value: str) -> str:

        #Обрезаем пробелы
        value = value.strip()

        #Проверяем что строка не пустая
        if not value:
            raise ValueError('Задайте имя кошелька')

        #Возвращаем очищенное значение
        return value






# класс создания кошелька
class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=30)
    initial_balance: Decimal = 0

    @field_validator('name')
    def name_not_empty(cls, value: str) -> str:
        # Обрезаем пробелы
        value = value.strip()

        # Проверяем что строка не пустая
        if not value:
            raise ValueError('Задайте имя кошелька')

        # Возвращаем очищенное значение
        return value

    @field_validator('initial_balance')
    def validate_initial_balance_positive(cls, value: Decimal) -> Decimal:
        # Проверка на отрицательное значение
        if value < 0:
            raise ValueError('Сумма должна быть положительной')
        # Возвращаем value
        return value



class UserRequest(BaseModel):
    login: str = Field(..., max_length=30)


class UserResponse(UserRequest):
    model_config = {'from_attributes': True}

    id: int
