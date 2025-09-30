from models.base_model import BaseModel
from datetime import datetime


class Order(BaseModel):
    def __init__(self, order_id, user_id, items, address, payment_method):
        super().__init__(order_id)
        self.user_id = user_id
        self.items = items
        self.address = address
        self.payment_method = payment_method
        self.total = self.calculate_total()
        self.status = "Обработва се"
        self.created_at = datetime.now()

    def calculate_total(self):
        return sum(item['product']['price'] * item['quantity'] for item in self.items)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'user_id': self.user_id,
            'items': self.items,
            'address': self.address,
            'payment_method': self.payment_method,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
        return base_dict