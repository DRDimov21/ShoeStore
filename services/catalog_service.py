from services.base_service import BaseService
from models.product_model import Product


class CatalogService(BaseService):
    def __init__(self):
        super().__init__()
        self._initialize_sample_products()

    def get_all(self):
        return [p for p in self.items if p.get_total_stock() > 0]

    def add_product(self, name, description, color, size, price, stock):
        product = Product(self._get_next_id(), name, description, color, size, price, stock)
        self.items.append(product)
        return product

    def update_product(self, product_id, name, description, color, size, price, stock):
        product = self.get_by_id(product_id)
        if product:
            product.name = name
            product.description = description
            product.color = color
            product.size = size
            product.price = price
            product.stock = stock
            return True
        return False

    def delete_product(self, product_id):
        product = self.get_by_id(product_id)
        if product:
            self.items.remove(product)
            return True
        return False

    def search_products(self, query):
        query = query.lower()
        return [p for p in self.items if
                query in p.name.lower() or
                query in p.color.lower() or
                query in p.description.lower()]

    def filter_products(self, products_list, color='', size='', max_price=''):
        filtered = products_list

        if color:
            filtered = [p for p in filtered if p.color.lower() == color.lower()]

        if size:
            filtered = [p for p in filtered if p.size == size]

        if max_price:
            filtered = [p for p in filtered if p.price <= float(max_price)]

        return filtered

    def decrease_stock(self, product_id, size, quantity):
        product = self.get_by_id(product_id)
        if product:
            return product.decrease_stock(size,quantity)
        return False

    def _initialize_sample_products(self):
        sample_products = [
            Product(self._get_next_id(), 'Nike Air Max', 'Спортни обувки за всеки ден',
                    'черни',["38", "39", "40", "41", "42", "43", "44", "45"], 199.99, 10),
            Product(self._get_next_id(), 'Adidas Ultraboost', 'Обувки за бягане',
                    'бели', ["38", "39", "40", "41", "42", "43", "44", "45"], 229.99, 8),
            Product(self._get_next_id(), 'Vans Old School', 'Класически кецове',
                    'черно-бели', ["38", "39", "40", "41", "42", "43", "44", "45"], 89.99, 15)
        ]

        self.items.extend(sample_products)




catalog_service = CatalogService()