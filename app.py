from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user
import json
from flask_socketio import SocketIO

from model.user import User
from model.game import Game

config = json.load(open("config.json", "r"))

app = Flask(__name__)
app.secret_key = config["secret_key"]

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

users = {}  # UID : User

games = {}  # language : (lesson url name : [game])


@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        users[user_id] = User(user_id)
    return users[user_id]


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@socketio.on('connected')
def connected():
    if current_user.is_authenticated:
        current_user.namespace = request.namespace


@socketio.on('disconnect')
def disconnect():
    current_user.namespace = None


@app.route('/')
@login_required
def hello_world():
    return render_template("index.html", user_data=current_user.lingo.data)


@app.route('/queue/<language>/<lesson_url_name>')
@login_required
def queue(language, lesson_url_name):
    if games.get(language) is None:
        games[language] = {}
    if games[language].get(lesson_url_name) is None:
        games[language][lesson_url_name] = Game(current_user)
        return render_template("queue.html", lesson_info=current_user.lingo.lesson_info[lesson_url_name])
    else:
        game = games[language][lesson_url_name]
        game.add_user(current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template("login.html")
    elif request.method == 'POST':
        user = load_user(request.values["username"])
        user.login(request.values["password"])
        if user.is_authenticated:
            login_user(user)
            return redirect('/')
        else:
            return redirect('/login')


if __name__ == '__main__':
    socketio.run(app)
