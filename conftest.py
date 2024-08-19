import pytest
import requests
from faker import Faker
from utils import register_user
from routes import USER_SETTINGS_DELETE, USER_REGISTER

fake = Faker()


@pytest.fixture(scope="function")
def create_ui_user(valid_user_data, delete_user):
    """
    Фикстура для создания пользователя для UI тестов.
    Генерирует уникального пользователя, возвращает данные и токены, а затем удаляет пользователя после теста.
    """
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

        assert response.status_code == 202
        assert response.json()["success"] is True
        assert response.json()["message"] == "User successfully removed"

    return _delete_user


@pytest.fixture
def valid_order_data():
    """Возвращает данные для успешного создания заказа с валидными ингредиентами."""
    return {
        "ingredients": ["61c0c5a71d1f82001bdaaa6c", "61c0c5a71d1f82001bdaaa73"]
    }


@pytest.fixture
def invalid_order_data():
    """Возвращает данные для создания заказа с невалидным хешем ингредиента."""
    return {
        "ingredients": ["invalidhash123", "609646e4dc916e00276b2870"]
    }


@pytest.fixture
def empty_order_data():
    """Возвращает данные для создания заказа без ингредиентов."""
    return {
        "ingredients": []
    }
