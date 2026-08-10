import pytest

import helpers
from api import LoginApi, UserApi, OrderApi


@pytest.fixture
def create_new_user_data():
    payload = helpers.create_new_user_data()

    yield payload

    # если пользователь с этими данными был создан - удаляем его
    login_response = LoginApi.login_user({
        'email': payload['email'],
        'password': payload['password'],
    })

    if login_response.status_code == 200:
        UserApi.delete_user(login_response.json()['accessToken'])


@pytest.fixture
def create_fake_email():
    payload = helpers.generate_email()

    yield payload


@pytest.fixture
def create_fake_password():
    payload = helpers.generate_password()

    yield payload


@pytest.fixture
def get_ingredients():
    ingredients = OrderApi.get_ingredients().json()['data']
    hashes = [item['_id'] for item in ingredients]

    yield hashes
