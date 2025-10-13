from models.base_model import BaseModel


class Product(BaseModel):
    def __init__(self, product_id, name, description, color, price, sizes_stock, image=None):
        super().__init__(product_id)
        self.name = name
        self.description = description
        self.color = color
        self.price = float(price)
        self.sizes_stock = sizes_stock
        self.image = image or 'default_shoe.jpg'

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'price': self.price,  # 👈 Вече е float
            'sizes_stock': self.sizes_stock,
            'image': self.image
        })
        return base_dict

    def get_available_sizes(self):

        if isinstance(self.sizes_stock, dict):
            return [size for size, stock in self.sizes_stock.items() if stock > 0]
        return []

    def decrease_stock(self, size, quantity):

        if (isinstance(self.sizes_stock, dict) and
                size in self.sizes_stock and
                self.sizes_stock[size] >= quantity):
            self.sizes_stock[size] -= quantity
            return True
        return False

    def get_total_stock(self):

        if isinstance(self.sizes_stock, dict):
            return sum(int(stock) for stock in self.sizes_stock.values())
        return 0