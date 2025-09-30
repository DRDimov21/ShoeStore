class BaseModel:


    def __init__(self, item_id):
        self.id = item_id

    def to_dict(self):
        return {'id': self.id}

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"