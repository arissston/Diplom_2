import allure
import pytest

from api import RegisterApi

# Создание пользователя:

# создать уникального пользователя;
# создать пользователя, который уже зарегистрирован;
# создать пользователя и не заполнить одно из обязательных полей.


class TestRegistration:

    @allure.title('Проверка, что успешно создаётся уникальный пользователь')
    def test_successful_registration_of_a_new_user(self, create_new_user_data):

        response = RegisterApi.create_user(create_new_user_data)

        assert response.status_code == 200
        assert 'accessToken' in response.json()

    @allure.title('Проверка, что нельзя создать дубль пользователя, который уже существует')
    def test_registration_of_an_already_existent_user(self, create_new_user_data):

        response_first = RegisterApi.create_user(create_new_user_data)
        assert response_first.status_code == 200

        response_second = RegisterApi.create_user(create_new_user_data)

        assert response_second.status_code == 403
        assert 'User already exists' in response_second.json()['message']

    @allure.title('Проверка, что если нет поля {field}, запрос на регистрацию возвращает 403 и сообщение об ошибке')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_registration_of_a_new_user_without_one_of_required_field(self, create_new_user_data, field):

        payload = {k: v for k, v in create_new_user_data.items() if k != field}

        response = RegisterApi.create_user(payload)

        assert response.status_code == 403
        assert 'Email, password and name are required fields' in response.json()['message']
