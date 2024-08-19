import pytest
import allure
from utils import register_user
from routes import USER_REGISTER
from messages import ERROR_MSG_USER_ALREADY_EXISTS, ERROR_MSG_MISSING_FIELDS


class TestUserRegistration:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_user_success(self, valid_user_data, delete_user):
        with allure.step("Регистрация нового пользователя"):
            response = register_user(USER_REGISTER, valid_user_data)
            data = response.json()

        with allure.step("Проверка успешного создания пользователя"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "user" in data
            assert data["user"]["email"] == valid_user_data["email"]
            assert data["user"]["name"] == valid_user_data["name"]

        with allure.step("Удаление пользователя после успешного создания"):
            delete_user(response.json()["accessToken"])

    @allure.title("Попытка создания пользователя, который уже существует")
    def test_create_user_already_exists(self, valid_user_data):
        with allure.step("Создание первого пользователя"):
            register_user(USER_REGISTER, valid_user_data)

        with allure.step("Попытка создания того же пользователя снова"):
            response = register_user(USER_REGISTER, valid_user_data)
            data = response.json()

        with allure.step("Проверка ошибки создания пользователя"):
            assert response.status_code == 403
            assert data["success"] is False
            assert data["message"] == ERROR_MSG_USER_ALREADY_EXISTS

    @pytest.mark.parametrize("user_data, expected_message", [
        ({"email": "missing_password@example.com", "name": "Test User"}, ERROR_MSG_MISSING_FIELDS),
        ({"password": "password123", "name": "Test User"}, ERROR_MSG_MISSING_FIELDS),
        ({"email": "missing_name@example.com", "password": "password123"}, ERROR_MSG_MISSING_FIELDS)
    ])
    @allure.title("Создание пользователя с отсутствующими полями")
    @allure.description("Проверка ошибки создания пользователя при отсутствии обязательных полей")
    def test_create_user_incomplete_fields(self, user_data, expected_message):
        with allure.step("Попытка регистрации пользователя с недостающими полями"):
            response = register_user(USER_REGISTER, user_data)
            data = response.json()

        with allure.step("Проверка ошибки при недостаточных данных"):
            assert response.status_code == 403
            assert data["success"] is False
            assert data["message"] == expected_message


