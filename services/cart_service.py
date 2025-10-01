from services.base_service import BaseService


class CartService(BaseService):
    def __init__(self):
        super().__init__()
        self.carts = {}

    def get_cart(self, user_id):
        return self.carts.get(user_id, [])

    def add_to_cart(self, user_id, product_id,size, quantity):

        from services.catalog_service import catalog_service

        product = catalog_service.get_by_id(product_id)
        if not product or product.stock < quantity:
            return False

        if size not in product.sizes_stock or product.sizes_stock[size] < quantity:
            return False

        if user_id not in self.carts:
            self.carts[user_id] = []


        for item in self.carts[user_id]:
            if item['product']['id'] == product_id and item['size'] == size:
                item['quantity'] += quantity
                return True


        self.carts[user_id].append({
            'product': product.to_dict(),
            'size': size,
            'quantity': quantity
        })
        return True

    def remove_from_cart(self, user_id, product_id):
        if user_id in self.carts:
            self.carts[user_id] = [item for item in self.carts[user_id]
                                   if item['product']['id'] != product_id]

    def clear_cart(self, user_id):
        if user_id in self.carts:
            self.carts[user_id] = []

    def get_cart_total(self, user_id):
        cart = self.get_cart(user_id)
        return sum(item['product']['price'] * item['quantity'] for item in cart)



cart_service = CartService()

