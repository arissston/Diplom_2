import allure
import requests

import urls


class RegisterApi:

    @staticmethod
    @allure.step('Регистрируем пользователя')
    def create_user(payload):
        return requests.post(urls.REGISTER_API, json=payload)


class UserApi:

    @staticmethod
    @allure.step('Удаляем пользователя')
    def delete_user(token):
        return requests.delete(urls.USER_API, headers={'Authorization': token})


class LoginApi:

    @staticmethod
    @allure.step('Логиним пользователя')
    def login_user(payload):
        return requests.post(urls.LOGIN_API, json=payload)


class OrderApi:

    @staticmethod
    @allure.step('Создаём заказ')
    def create_order(payload, token=None):
        headers = {'Authorization': token} if token else {}
        return requests.post(urls.ORDERS_API, json=payload, headers=headers)

    @staticmethod
    @allure.step('Запрашиваем список ингредиентов')
    def get_ingredients():
        return requests.get(urls.INGREDIENTS_API)
