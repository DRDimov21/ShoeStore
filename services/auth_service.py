from models.users_model import User
from services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self):
        super().__init__()
        self._create_default_admin()

    def register_user(self, email, password, name):
        if any(user.email == email for user in self.items):
            return None

        user = User(self._get_next_id(), email, password, name)
        self.items.append(user)
        return user

    def login_user(self, email, password):
        return next((user for user in self.items
                     if user.email == email and user.password == password), None)

    def _create_default_admin(self):
        admin_user = User(self._get_next_id(), 'admin@shoestore.com', 'admin123',
                          'Администратор', True)
        self.items.append(admin_user)



auth_service = AuthService()