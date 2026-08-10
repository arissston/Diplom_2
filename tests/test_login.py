import allure
import pytest

from api import RegisterApi, LoginApi

MISSING = object()

# Логин пользователя:

# вход под существующим пользователем;
# вход с неверным логином и паролем.


class TestLogin:

    @allure.title('Проверка, что можно успешно залогиниться под существующим пользователем')
    def test_successful_login_for_existent_user(self, create_new_user_data):

        register_response = RegisterApi.create_user(create_new_user_data)
        assert register_response.status_code == 200

        response = LoginApi.login_user(create_new_user_data)

        assert response.status_code == 200
        assert 'accessToken' in response.json()

    @allure.title('Проверка, что при входе с неверными данными: {email} / {password} - возвращается 401 и текст ошибки')
    @pytest.mark.parametrize("email, password",
                             [
                                 ("wrong_email", "wrong_password"),
                                 ("wrong_email", "real_password"),
                                 ("real_email", "wrong_password"),
                                 ("empty_email", "real_password"),
                                 ("real_email", "empty_password"),
                                 ("empty_email", "empty_password"),
                                 ("no_email",    "real_password"),
                                 ("real_email",  "no_password"),
                                 ("no_email",    "no_password")
                             ])
    def test_login_with_wrong_credentials_returns_401(self, create_new_user_data, create_fake_email,
                                                      create_fake_password, email, password):

        register_response = RegisterApi.create_user(create_new_user_data)
        assert register_response.status_code == 200

        emails = {
            'real_email':  create_new_user_data['email'],
            'wrong_email': create_fake_email,
            'empty_email': '',
            'no_email':    MISSING,
        }
        passwords = {
            'real_password':  create_new_user_data['password'],
            'wrong_password': create_fake_password,
            'empty_password': '',
            'no_password':    MISSING,
        }

        data = {
            key: value
            for key, value in (('email', emails[email]), ('password', passwords[password]))
            if value is not MISSING
        }

        response = LoginApi.login_user(data)

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}."
        assert 'email or password are incorrect' in response.json()['message'], f"Ошибка: {response.json()['message']}"
