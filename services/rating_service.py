from models.rating_model import Rating
from services.base_service import BaseService


class RatingService(BaseService):
    def __init__(self):
        super().__init__()

    def add_rating(self, product_id, user_id, rating, comment=None):
        """Добавя рейтинг и коментар за продукт"""
        # Конвертиране към string за сигурност в сравненията
        product_id_str = str(product_id)
        user_id_str = str(user_id)

        # Проверка дали потребителят вече е оценил този продукт
        existing_rating = self.get_user_rating_for_product(product_id_str, user_id_str)

        if existing_rating:
            # Ако има вече оценка - ъпдейтваме я
            existing_rating.rating = rating
            existing_rating.comment = comment
            return existing_rating

        # Създаване на нов рейтинг
        new_rating = Rating(
            rating_id=self._get_next_id(),
            product_id=product_id_str,
            user_id=user_id_str,
            rating=rating,
            comment=comment
        )
        self.items.append(new_rating)
        return new_rating

    def get_user_rating_for_product(self, product_id, user_id):
        """Връща рейтинга на конкретен потребител за конкретен продукт"""
        for rating in self.items:
            # Сравняваме като strings за да избегнем проблеми с типовете
            if (str(rating.product_id) == str(product_id) and
                    str(rating.user_id) == str(user_id)):
                return rating
        return None

    def get_ratings_for_product(self, product_id):
        """Връща всички рейтинги за даден продукт"""
        product_id_str = str(product_id)
        return [r for r in self.items if str(r.product_id) == product_id_str]

    def get_average_rating(self, product_id):
        ratings = self.get_ratings_for_product(product_id)
        if not ratings:
            return 0

        total = sum(r.rating for r in ratings)
        return round(total / len(ratings), 1)

    def get_rating_stats(self, product_id):
        ratings = self.get_ratings_for_product(product_id)
        if not ratings:
            return {
                'average': 0,
                'count': 0,
                'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }

        total = sum(r.rating for r in ratings)
        average = round(total / len(ratings), 1)

        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for r in ratings:
            distribution[r.rating] += 1

        return {
            'average': average,
            'count': len(ratings),
            'distribution': distribution
        }


rating_service = RatingService()