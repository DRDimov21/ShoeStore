# Данни в паметта
orders = []
next_order_id = 1


def create_order(user_id, address, payment_method):
    global next_order_id
    from services.cart_service import get_cart
    from services.catalog_service import decrease_stock

    cart = get_cart(user_id)
    if not cart:
        return None

    # Проверка за наличност
    for item in cart:
        if not decrease_stock(item['product']['id'], item['quantity']):
            return None

    order = {
        'id': next_order_id,
        'user_id': user_id,
        'items': cart.copy(),
        'address': address,
        'payment_method': payment_method,
        'total': sum(item['product']['price'] * item['quantity'] for item in cart),
        'status': 'Обработва се'
    }

    orders.append(order)
    next_order_id += 1
    return order


def get_orders_by_user(user_id):
    return [order for order in orders if order['user_id'] == user_id]


def get_all_orders():
    return orders


def get_order_by_id(order_id):
    return next((order for order in orders if order['id'] == order_id), None)