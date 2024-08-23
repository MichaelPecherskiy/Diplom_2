
def valid_order_data():
    """Возвращает данные для успешного создания заказа с валидными ингредиентами."""
    return {
        "ingredients": ["61c0c5a71d1f82001bdaaa6c", "61c0c5a71d1f82001bdaaa73"]
    }


def invalid_order_data():
    """Возвращает данные для создания заказа с невалидным хешем ингредиента."""
    return {
        "ingredients": ["invalidhash123", "609646e4dc916e00276b2870"]
    }


def empty_order_data():
    """Возвращает данные для создания заказа без ингредиентов."""
    return {
        "ingredients": []
    }