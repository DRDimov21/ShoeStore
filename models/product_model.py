from sqlalchemy.testing.util import total_size

from models.base_model import BaseModel


class Product(BaseModel):
    def __init__(self, product_id, name, description, color, sizes_stock, price, stock):
        super().__init__(product_id)
        self.name = name
        self.description = description
        self.color = color
        self.sizes_stock = sizes_stock
        self.price = price
        self.stock = stock

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'sizes_stock': self.sizes_stock,
            'price': self.price,
            'stock': self.stock
        })
        return base_dict

    def get_available_sizes(self):
        return [size for size, stock in self.sizes_stock.items() if stock > 0]

    def decrease_stock(self, size, quantity):
        if size in self.sizes_stock and self.sizes_stock[size] >= quantity:
            self.sizes_stock[size] -= quantity
            return True
        return False

    def get_total_stock(self):
        total = 0
        try:
            if isinstance(self.sizes_stock, list):
                for item in self.sizes_stock:
                    try:
                        total += int(item)
                    except (ValueError, TypeError):
                        continue

            elif isinstance(self.sizes_stock, dict):
                for stock in self.sizes_stock.values():
                    try:
                        total += int(stock)
                    except (ValueError, TypeError):
                        continue
            else:
                return 10
        except Exception as e:
            return 10

        return total if total > 0 else 10