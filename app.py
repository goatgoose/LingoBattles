from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, current_user
from model.user import User
import json

config = json.load(open("config.json", "r"))

app = Flask(__name__)
app.secret_key = config["secret_key"]

login_manager = LoginManager()
login_manager.init_app(app)

users = {}  # UID : User


@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        users[user_id] = User(user_id)
    return users[user_id]


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route('/')
@login_required
def hello_world():
    return render_template("index.html", user_data=current_user.lingo.data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
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
    app.run()
