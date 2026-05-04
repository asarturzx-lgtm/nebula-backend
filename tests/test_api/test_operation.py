from decimal import Decimal

from app.models import User, Wallet



# тест ручки на вывод
def test_add_expense_success(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    response = client.post('/api/v1/operations/expense', json={
        'wallet_name': 'card',
        'amount': 100,
        'destination': 'Food',
    },
                           headers={'authorization': f'Bearer {user.login}'})

    assert response.status_code == 200
    assert response.json()['massage'] == 'Вывод средств выполнен успешно'
    assert response.json()['wallet_name'] == wallet.name
    assert Decimal(str(response.json()['amount'])) == Decimal(100)
    assert Decimal(str(response.json()['balance'])) == Decimal(100)
    assert response.json()['destination'] == 'Food'



#тест на вывод отрицательной суммы
def test_add_expense_negative(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post('/api/v1/operations/expense', json={
        'wallet_name': 'card',
        'amount': -100,
        'destination': 'Food',
    },  headers={'authorization': f'Bearer {user.login}'})

    assert response.status_code == 422



#тест на кошелек c пробелами
def test_add_expense_wallet_no(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    response = client.post('/api/v1/operations/expense', json={
        'wallet_name': '    ',
        'amount': -100,
        'destination': 'Food',
    },  headers={'authorization': f'Bearer {user.login}'})

    assert response.status_code == 422



#тест на кошелек который не существует
def test_add_expense_wallet_not_foud(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.commit()

    response = client.post('/api/v1/operations/expense', json={
        'wallet_name': 'card',
        'amount': 100,
        'destination': 'Food',
    },  headers={'authorization': f'Bearer {user.login}'})

    assert response.status_code == 404


#тест на авторизацию
def test_add_expense_authorization(db_session, client):


    response = client.post('/api/v1/operations/expense', json={
        'wallet_name': 'card',
        'amount': 100,
        'destination': 'Food',
    },  headers={'authorization': f'Bearer {'notexists'}'})

    assert response.status_code == 401



# тест на вывод больше баланса
def test_add_expense_over_money(db_session, client):
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name='card', balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    response = client.post('/api/v1/operations/expense', json={
        'wallet_name': 'card',
        'amount': 1000,
        'destination': 'Food',
    },
                           headers={'authorization': f'Bearer {user.login}'})

    assert response.status_code == 400