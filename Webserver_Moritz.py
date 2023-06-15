from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

from flask import Flask, render_template, request, redirect, url_for, flash
import db_connection
from Tools import hash_password
from player_class import Player
from user_class import User
from Control import control


players = []
app = Flask(__name__)
control = control()
player = None
app.secret_key = 'sventegetscookie'
socketio = SocketIO(app)
online_users = []

app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
            username = request.form.get('username')
            hashed_password = hash_password(request.form.get('password'))
            if db_connection.check_login(username, hashed_password):
                return redirect('/startPage')
            else:
                error_message = "Benutzername oder Passwort falsch"  # Fehlermeldung
                return render_template('index.html', error_message=error_message)
    else:
        return render_template('index.html')


@app.route('/registrierung', methods=['GET', 'POST'])
def registrierung():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('vor_name')
        last_username = request.form.get('last_name')
        birthday = request.form.get('birthdaytime')
        today = datetime.now()
        birthday_object = datetime.fromisoformat(birthday)
        age = (today.day - birthday_object.day)/365
        if age<18:
            print(age)
            return redirect("/")
        hashed_password = hash_password(request.form.get('password'))

        if db_connection.check_username(username):
            error_message = "Benutzernamen bereits vergeben"  # Fehlermeldung
        else:
            new_user = User(username, hashed_password)
            flash("Registrierung erfolgreich, bitte melden Sie sich an")
            return redirect("/")

    return render_template('registrierung.html')


@app.route('/startPage', methods=['GET', 'POST'])
def random_session():

    if request.method == 'POST':
        control.choose_session(player)
        print(control.session_list[-1].player_list)
        return redirect('/game_template')
    # name = request.form.get('name')  #
    # session['name'] = name  # LOBBY TEST
    # print(name)  #
    return render_template('startPage.html')


@app.route('/game_template', methods=['GET', 'POST'])
def game():
    return render_template('game_template.html')


# -------- LOBBY TEST ---------
@app.route('/display', methods=['POST'])
def display():
    name = session.get('name')
    return render_template('display.html', name=name)

@app.route('/users')
def users():
    return render_template('users.html')

@socketio.on('connect')
def handle_connect():
    name = session.get('name')
    online_users.append(name)
    emit('user_update', online_users, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    name = session.get('name')
    if name in online_users:
        online_users.remove(name)
    emit('user_update', online_users, broadcast=True)

# ------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='81', debug=True)
