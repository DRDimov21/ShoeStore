from models.base_model import BaseModel


class Product(BaseModel):
    def __init__(self, product_id, name, description, color, size, price, stock):
        super().__init__(product_id)
        self.name = name
        self.description = description
        self.color = color
        self.size = size
        self.price = price
        self.stock = stock

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'size': self.size,
            'price': self.price,
            'stock': self.stock
        })
        return base_dict

    def decrease_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False