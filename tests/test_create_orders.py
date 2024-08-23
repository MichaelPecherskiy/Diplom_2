import allure
from utils import create_order
from messages import ERROR_MSG_MISSING_INGREDIENTS
from routes import ORDERS
from constants import valid_order_data, invalid_order_data, empty_order_data


@allure.epic("Order Management")
@allure.suite("Order Creation")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными данными")
    def test_create_order_with_auth(self, create_user_and_get_tokens, delete_user):
        with allure.step("Регистрация нового пользователя и получение токенов"):
            tokens = create_user_and_get_tokens
            access_token = tokens["accessToken"]

        with allure.step("Создание заказа с использованием токена"):
            response = create_order(ORDERS, access_token, valid_order_data())
            data = response.json()

        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            assert data["success"] is True, "Поле 'success' должно быть True"
            assert "order" in data, "Ответ не содержит поле 'order'"
            assert "number" in data["order"], "Ответ не содержит поле 'number' в 'order'"

        with allure.step("Удаление пользователя после теста"):
            delete_user(access_token)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_data(self):
        with allure.step("Попытка создать заказ без авторизации"):
            response = create_order(ORDERS, None, empty_order_data())
            data = response.json()

        with allure.step("Проверка ответа с ошибкой 400"):
            assert response.status_code == 400
            assert data["success"] is False
            assert data["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user_and_get_tokens):
        with allure.step("Получение токенов"):
            tokens = create_user_and_get_tokens
            access_token = tokens["accessToken"]

        with allure.step("Попытка создания заказа с пустым списком ингредиентов"):
            response = create_order(ORDERS, access_token, empty_order_data())
            data = response.json()

        with allure.step("Проверка ответа с ошибкой 400"):
            assert response.status_code == 400  # Обычно ошибки валидации возвращаются с кодом 400
            assert data["success"] is False
            assert data["message"] == ERROR_MSG_MISSING_INGREDIENTS

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients_hash(self, create_user_and_get_tokens):
        with allure.step("Получение токенов"):
            tokens = create_user_and_get_tokens
            access_token = tokens["accessToken"]

        with allure.step("Попытка создания заказа с невалидными хешами ингредиентов"):
            response = create_order(ORDERS, access_token, invalid_order_data())

        with allure.step("Проверка, что сервер возвращает код ошибки 500"):
            assert response.status_code == 500, "Ожидался статус-код 500, но получен другой статус"

        with allure.step("Проверка, что тело ответа содержит информацию о внутренней ошибке"):
            assert "Internal Server Error" in response.text, "Текст ошибки в ответе не содержит 'Internal Server Error'"

