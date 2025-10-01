from services.base_service import BaseService
from models.order_model import Order


class OrderService(BaseService):
    def __init__(self):
        super().__init__()
        self.cart_service = None
        self.catalog_service = None

    def set_services(self, cart_service, catalog_service):
        self.cart_service = cart_service
        self.catalog_service = catalog_service

    def create_order(self, user_id, address, payment_method):
        if not self.cart_service or not self.catalog_service:
            return None

        cart_items = self.cart_service.get_cart(user_id)
        if not cart_items:
            return None


        for item in cart_items:
            if not self.catalog_service.decrease_stock(item['product']['id'], item['size'],item['quantity']):
                return None

        order = Order(self._get_next_id(), user_id, cart_items, address, payment_method)
        self.items.append(order)


        self.cart_service.clear_cart(user_id)

        return order

    def get_orders_by_user(self, user_id):
        return [order for order in self.items if order.user_id == user_id]



order_service = OrderService()