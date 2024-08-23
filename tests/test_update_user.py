import pytest
import allure
from utils import update_user_data
from routes import USER_SETTINGS_DELETE
from messages import ERROR_MSG_SHOUlD_BE_AUTH


@allure.epic("User Data Management")
@allure.suite("User Settings")
class TestUserSettings:

    @allure.title("Изменение данных пользователя с авторизацией")
    @allure.description("Проверяем возможность изменения данных пользователя при наличии авторизации.")
    def test_update_user_with_auth(self, create_user_and_get_tokens, updated_user_data, delete_user):
        with allure.step("Получение токена доступа для авторизованного пользователя"):
            tokens = create_user_and_get_tokens
            access_token = tokens["accessToken"]

        with allure.step("Обновление данных пользователя"):
            response = update_user_data(USER_SETTINGS_DELETE, access_token, updated_user_data)
            data = response.json()

        with allure.step("Проверка успешного обновления данных"):
            assert response.status_code == 200
            assert data["success"] is True
            assert data["user"]["email"] == updated_user_data["email"]
            assert data["user"]["name"] == updated_user_data["name"]

        with allure.step("Удаление пользователя после теста"):
            delete_user(access_token)

    @pytest.mark.parametrize("updated_data", [
        {"email": "new-email@example.com", "name": "New Name"},
        {"password": "newpassword123"},
        {"email": "another-email@example.com", "password": "anotherpassword123", "name": "Another Name"}
    ])
    @allure.title("Попытка изменения данных пользователя без авторизации")
    @allure.description("Проверяем попытку изменения данных пользователя без авторизации.")
    def test_update_user_without_auth_param(self, updated_data):
        with allure.step("Попытка обновления данных пользователя без токена авторизации"):
            response = update_user_data(USER_SETTINGS_DELETE, None, updated_data)
            data = response.json()

        with allure.step("Проверка отказа в доступе без авторизации"):
            assert response.status_code == 401
            assert data["success"] is False
            assert data["message"] == ERROR_MSG_SHOUlD_BE_AUTH



