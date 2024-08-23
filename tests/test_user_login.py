import allure
from messages import ERROR_MSG_EMAIL_OR_DATA_INCORRECT
from utils import create_and_login_user, get_invalid_login_data, login_user
from routes import USER_LOGIN


class TestLogin:

    @allure.title("Успешный логин под существующим пользователем")
    def test_login_success(self, delete_user):
        with allure.step("Создание и логин пользователя"):
            login_data = create_and_login_user()

        with allure.step("Выполнение логина"):
            response = login_user(USER_LOGIN, login_data)
            data = response.json()

        with allure.step("Проверка успешного логина"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "accessToken" in data
            assert "refreshToken" in data
            assert data["user"]["email"] == login_data["email"]
            assert data["user"]["name"] == "UniqueUser"

        with allure.step("Удаление пользователя после успешного логина"):
            delete_user(data["accessToken"])

    @allure.title("Неудачный логин с неверными данными")
    def test_login_failure(self):
        with allure.step("Получение неверных данных для логина"):
            login_data = get_invalid_login_data()

        with allure.step("Выполнение логина"):
            response = login_user(USER_LOGIN, login_data)
            data = response.json()

        with allure.step("Проверка отказа в логине"):
            assert response.status_code == 401
            assert data["success"] is False
            assert data["message"] == ERROR_MSG_EMAIL_OR_DATA_INCORRECT



