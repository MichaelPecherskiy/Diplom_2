import pytest
import requests
from faker import Faker
from utils import register_user
from routes import USER_SETTINGS_DELETE, USER_REGISTER

fake = Faker()


@pytest.fixture(scope="function")
def create_ui_user(valid_user_data, delete_user):
    # Регистрация пользователя и получение токенов
    response = register_user(USER_REGISTER, valid_user_data)
    data = response.json()
    user_info = {
        "email": valid_user_data["email"],
        "password": valid_user_data["password"],
        "name": valid_user_data["name"],
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"]
    }


@pytest.fixture
def unique_email():
    """Генерирует уникальный email для тестов."""
    return fake.email()


@pytest.fixture
def valid_user_data(unique_email):
    """Возвращает корректные данные пользователя с уникальным email."""
    return {
        "email": unique_email,
        "password": fake.password(length=12),
        "name": fake.name()
    }


@pytest.fixture
def updated_user_data():
    """Возвращает новые данные для обновления пользователя."""
    return {
        "email": fake.email(),
        "password": fake.password(length=12),
        "name": fake.name()
    }


@pytest.fixture
def create_user_and_get_tokens(valid_user_data):
    """Создает пользователя и возвращает его accessToken и refreshToken."""
    response = register_user(USER_REGISTER, valid_user_data)
    data = response.json()
    tokens = {
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"]
    }
    return tokens


@pytest.fixture
def incomplete_user_data():
    """Возвращает данные пользователя с отсутствующими полями."""
    return [
        {"email": fake.email(), "name": fake.name()},
        {"password": fake.password(length=12), "name": fake.name()},
        {"email": fake.email(), "password": fake.password(length=12)}
    ]


@pytest.fixture
def delete_user():
    """Удаляет пользователя по его accessToken."""

    def _delete_user(access_token):
        headers = {"Authorization": access_token}
        response = requests.delete(USER_SETTINGS_DELETE, headers=headers)
        return response

    return _delete_user

