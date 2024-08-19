import pytest
import allure
from utils import get_user_orders, create_order
from routes import ORDERS
from messages import ERROR_MSG_SHOUlD_BE_AUTH


@allure.epic("User Orders")
@allure.suite("Order Management")
class TestUserOrders:

    @pytest.mark.parametrize("order_data", [
        {"ingredients": ["61c0c5a71d1f82001bdaaa6c", "61c0c5a71d1f82001bdaaa73"]}
    ])
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_authorized(self, order_data, create_user_and_get_tokens, delete_user):
        with allure.step("Создание пользователя и получение токенов"):
            tokens = create_user_and_get_tokens
            access_token = tokens["accessToken"]

        with allure.step("Создание заказа"):
            create_order(ORDERS, access_token, order_data)

        with allure.step("Получение заказов пользователя"):
            response = get_user_orders(ORDERS, access_token)
            data = response.json()

        with allure.step("Проверка успешности запроса"):
            assert response.status_code == 200
            assert data["success"] is True
            assert "orders" in data
            assert len(data["orders"]) > 0

        with allure.step("Удаление пользователя после теста"):
            delete_user(access_token)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_unauthorized(self, invalid_order_data):
        with allure.step("Попытка получить заказы без авторизации"):
            response = get_user_orders(ORDERS, None)
            data = response.json()

        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == 401
            assert data["success"] is False
            assert data["message"] == ERROR_MSG_SHOUlD_BE_AUTH

