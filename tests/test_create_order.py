import allure
import pytest

from helpers import generate_fake_hash
from api import RegisterApi, LoginApi, OrderApi

# Создание заказа:

# с авторизацией;
# без авторизации;

# без ингредиентов;
# с неверным хешем ингредиентов.


class TestCreateOrder:

    @allure.title('Проверка, что успешно создаётся заказ с авторизацией пользователя и с ингредиентами')
    def test_successful_order_with_logged_in_user(self, create_new_user_data, get_ingredients):

        response_reg = RegisterApi.create_user(create_new_user_data)
        assert response_reg.status_code == 200

        login_response = LoginApi.login_user(create_new_user_data)
        assert login_response.status_code == 200

        token = login_response.json()['accessToken']

        response = OrderApi.create_order({'ingredients': get_ingredients[:3]}, token)

        assert response.status_code == 200
        assert 'number' in response.json()["order"]
        assert 'owner' in response.json()["order"]

    @allure.title('Проверка, что успешно создаётся заказ без авторизации пользователя и с ингредиентами')
    def test_successful_order_without_logged_in_user(self, get_ingredients):

        response = OrderApi.create_order({'ingredients': get_ingredients[:3]})

        assert response.status_code == 200
        assert 'number' in response.json()["order"]

    @allure.title('Проверка, что при попытке заказа без ингредиентов ({payload}) - вернётся ошибка 400')
    @pytest.mark.parametrize('payload', [{'ingredients': []}, {}])
    def test_order_without_ingredients_returns_400_and_error_message(self, payload):

        response = OrderApi.create_order(payload)

        assert response.status_code == 400
        assert 'Ingredient ids must be provided' in response.json()["message"]

    @allure.title('Проверка, что при попытке заказа с неверным хешем ингредиентов (верный формат) - будет ошибка 400')
    def test_order_with_wrong_hashes_and_correct_format_returns_400(self):

        response = OrderApi.create_order({'ingredients': [generate_fake_hash()]})

        assert response.status_code == 400
        assert 'One or more ids provided are incorrect' in response.json()["message"]

    @allure.title('Проверка, что при попытке заказа с хешем ингредиентов неправильного формата - вернётся ошибка 500')
    def test_order_with_wrong_format_hashes_returns_500(self):

        response = OrderApi.create_order({'ingredients': ["abc"]})

        assert response.status_code == 500
        assert 'Internal Server Error' in response.text
