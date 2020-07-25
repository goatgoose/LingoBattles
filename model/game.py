

class Game:
    def __init__(self, owner):
        self.owner = owner

        self.users = []
        self.add_user(self.owner)

    def add_user(self, user):
        self.users.append(user)

    def get_next_round(self):
        pass
