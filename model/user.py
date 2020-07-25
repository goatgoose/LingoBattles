from flask_login import UserMixin, login_user
import duolingo
from flask_socketio import emit


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.lingo = None
        self._is_authenticated = False

        self.sid = None
        self.current_game = None

    def login(self, password):
        try:
            self.lingo = duolingo.Duolingo(self.username, password)
            self._is_authenticated = True
        except duolingo.DuolingoException:
            print("Could not authenticate user: " + self.username)

    @property
    def is_active(self):
        return self._is_authenticated

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
