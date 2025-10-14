from models.base_model import BaseModel
import datetime

class Rating(BaseModel):
    def __init__(self, rating_id, product_id, user_id, rating, comment=None):
        super().__init__(rating_id)
        self.product_id = str(product_id)  # Винаги пазим като string
        self.user_id = str(user_id)        # Винаги пазим като string
        self.rating = int(rating)          # Винаги като integer
        self.comment = comment
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'product_id': self.product_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        })
        return base_dict