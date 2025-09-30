from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, user_id, email, password, name, is_admin=False):
        super().__init__(user_id)
        self.email = email
        self.password = password
        self.name = name
        self.is_admin = is_admin

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'is_admin': self.is_admin
        })
        return base_dict