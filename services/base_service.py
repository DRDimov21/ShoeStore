class BaseService:


    def __init__(self):
        self.items = []
        self.next_id = 1

    def get_all(self):

        return self.items

    def get_by_id(self, item_id):

        return next((item for item in self.items if item.id == item_id), None)

    def _get_next_id(self):

        current_id = self.next_id
        self.next_id += 1
        return current_id