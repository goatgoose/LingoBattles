import uuid


class Game:
    def __init__(self, socketio, owner, lesson_name):
        self.socketio = socketio
        self.owner = owner
        self.lesson_name = lesson_name

        self.id = str(uuid.uuid1())

        self.users = []
        self.points = {}  # user : points
        self.ready = {}  # user : ready/not ready
        self.add_user(self.owner)

        self.lesson = self.owner.lingo.get_lesson(self.lesson_name)
        self.current_challenge = -1
        self.challenge_count = len(self.lesson["challenges"])
        self.users_in_round = set()

    def add_user(self, user):
        self.users.append(user)
        self.points[user] = 0
        self.ready[user] = False

    def set_ready(self, user):
        self.ready[user] = True

    @property
    def all_ready(self):
        for ready in self.ready.values():
            if not ready:
                return False
        return True

    @property
    def winner(self):
        if len(self.users) == 0:
            return None

        winner_user = self.users[0]
        for user in self.users:
            if self.points[user] > self.points[winner_user]:
                winner_user = user
        return winner_user

    def start_round(self):
        self.users_in_round = set(self.users)
        self.current_challenge += 1
        if self.current_challenge >= self.challenge_count:
            for user in self.users:
                self.socketio.emit("game_end", {
                    "winner": self.winner.username
                }, room=user.sid)
        else:
            for user in self.users:
                self.socketio.emit("challenge",
                                   self.lesson["challenges"][self.current_challenge],
                                   room=user.sid)

    def submit_solution(self, user, challenge, solution):
        if challenge != self.current_challenge:
            return

        if solution in self.lesson["challenges"][self.current_challenge]["correctSolutions"]:
            self.points[user] += 1
            self.start_round()
            return

        self.users_in_round.remove(user)
        if len(self.users_in_round) == 1:
            self.points[self.users_in_round.pop()] += 1
            self.start_round()
