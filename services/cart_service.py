# Данни в паметта
carts = {}


def get_cart(user_id):
    return carts.get(user_id, [])


def add_to_cart(user_id, product_id, quantity):
    from services.catalog_service import get_product_by_id

    product = get_product_by_id(product_id)
    if not product or product['stock'] < quantity:
        return False

    if user_id not in carts:
        carts[user_id] = []

    # Проверка дали продуктът вече е в кошницата
    for item in carts[user_id]:
        if item['product']['id'] == product_id:
            item['quantity'] += quantity
            return True

    # Добавяне на нов продукт
    carts[user_id].append({
        'product': product,
        'quantity': quantity
    })
    return True


def remove_from_cart(user_id, product_id):
    if user_id in carts:
        carts[user_id] = [item for item in carts[user_id] if item['product']['id'] != product_id]


def clear_cart(user_id):
    if user_id in carts:
        carts[user_id] = []


def get_cart_total(user_id):
    cart = get_cart(user_id)
    return sum(item['product']['price'] * item['quantity'] for item in cart)