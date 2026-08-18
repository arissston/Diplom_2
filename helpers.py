from faker import Faker


fake = Faker()


def generate_email():
    return f"{fake.uuid4()[:8]}@testburger.ru"


def generate_password():
    return fake.password(length=8)


def generate_first_name():
    return fake.first_name()


# метод создаёт данные пользователя, для использования другими методами
def create_new_user_data():
    # генерируем имя, логин (*email в данном случае) и пароль - и возвращаем данные
    payload = {
        "email": generate_email(),
        "password": generate_password(),
        "name": generate_first_name(),
    }

    return payload


def generate_fake_hash():
    return fake.hexify(text="^" * 24)
