import uuid


class Game:
    def __init__(self, owner):
        self.owner = owner

        self.id = str(uuid.uuid1())

        self.users = []
        self.add_user(self.owner)

    def add_user(self, user):
        self.users.append(user)

    def get_next_round(self):
        pass
