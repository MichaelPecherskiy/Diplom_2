import requests
from routes import USER_REGISTER


def register_user(base_url, user_data):
    return requests.post(base_url, json=user_data)


def login_user(url, login_data):
    """Функция для логина пользователя."""
    return requests.post(url, json=login_data)


def update_user_data(url, token, new_data, old_password=None):
    """Функция для обновления данных пользователя."""
    headers = {"Authorization": token}
    if "password" in new_data and old_password:
        new_data["oldPassword"] = old_password
    return requests.patch(url, headers=headers, json=new_data)


def create_and_login_user():
    """Регистрирует нового пользователя и возвращает его данные для логина."""
    user_data = {
        "email": "test-user-unique@example.com",
        "password": "password",
        "name": "UniqueUser"
    }
    register_user(USER_REGISTER, user_data)
    return {
        "email": user_data["email"],
        "password": user_data["password"]
    }


def get_invalid_login_data():
    """Возвращает данные для неудачного логина (неправильные логин и пароль)."""
    return {
        "email": "wrong-email@yandex.ru",
        "password": "wrongpassword"
    }


def create_order(url, access_token, order_data):
    """Функция для создания заказа."""
    headers = {
        "Authorization": f"{access_token}",  # Исправляем формат
        "Content-Type": "application/json"
    }
    print("Заголовки запроса:", headers)  # Принт заголовков
    response = requests.post(url, headers=headers, json=order_data)
    print("Ответ сервера:", response.status_code, response.text)  # Принт ответа
    return response


def get_user_orders(url, access_token):
    """Функция для получения заказов пользователя."""
    headers = {
        "Authorization": f"{access_token}" if access_token else None,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response
