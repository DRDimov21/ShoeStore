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
        if isinstance(self.sizes_stock, list):
            return sum(self.sizes_stock)
        elif isinstance(self.sizes_stock, dict):
            return sum(int(stock) for stock in self.sizes_stock.values())
        else:
            return 0

