from datetime import datetime
import socketio
from flask import Flask, render_template, request, redirect, flash, session
from flask_socketio import SocketIO, emit

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
lobbies = {}
users_dict={}
users_dict["open_lobbies"] = {}

app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        username = request.form.get('username')
        hashed_password = hash_password(request.form.get('password'))
        if db_connection.check_login(username, hashed_password):
            session['username']=username
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
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthdaytime')
        today = datetime.now()
        birthday_object = datetime.fromisoformat(birthday)
        age = (today.year - birthday_object.year)
        if (today.month, today.day) < (birthday_object.month, birthday_object.day):
            age -= 1
        if age < 18:
            return render_template('registrierung.html',
                                   error_message="Regestrierung fehlgeschlagen,das Mindestalter ist 18 Jahre")
        hashed_password = hash_password(request.form.get('password'))

        if db_connection.check_username(username):
            return render_template('registrierung.html', error_message="Der Username ist bereits vergeben")
        else:
            birthday_formatted = birthday_object.strftime('%Y-%m-%d')
            print(birthday_formatted)
            new_user = User(username, hashed_password, first_name, last_name, birthday_formatted)
            flash("Registrierung erfolgreich, bitte melden Sie sich an")
            return redirect("/")

    return render_template('registrierung.html')

# WICHTIG
@app.route('/startPage', methods=['GET', 'POST'])
def random_session():

    username = session['username']
    users_dict[username] = Player(username)

    if request.method == 'POST':

        # if request.form['btn'] == 'Zufälligem Spiel beitreten':
        #     return redirect('/game_template')

        if request.form['btn'] == 'Spiel hosten':
            users_dict["open_lobbies"][username]=[Player(username)]
            return redirect(f'/users/{username}')

        if request.form['btn'] == 'Spiel beitreten':
            return redirect('/lobby_list')

    return render_template('startPage.html', username=username, credit=users_dict[username].credit)


@app.route('/game_template', methods=['GET', 'POST'])
def game():

    if request.method == 'POST':
        pass

    return render_template('game_template.html')

# WICHTIG (villeicht)
@app.route('/users', methods=['POST', 'GET'])
def users():
    username = session.get('username')

    if request.method == 'POST':
        return redirect('/startPage')

    return render_template('users.html', username=username)

# WICHTIG
@app.route('/lobby_list', methods=['POST', 'GET'])
def lobbies():

    username = session.get('username')
    lobbies=users_dict["open_lobbies"].keys()
    lobbies=list(lobbies)

    if request.method == 'POST':

        for element in lobbies:
            if request.form['btn'] == f"{element} beitreten":
                users_dict["open_lobbies"][element].append(users_dict[username])
                return redirect(f'/users/{element}')
    return render_template('lobby_list.html', lobbies=lobbies)

# WICHTIG
@app.route('/users/<irgendeine_variable>')
def personal_lobby(irgendeine_variable):

    username = session.get('username')
    onlineUsersList = users_dict["open_lobbies"][irgendeine_variable]

    print(irgendeine_variable)

    players = []

    print(users_dict)

    for element in users_dict["open_lobbies"][irgendeine_variable]:
        players.append(element.username)

    print(players)

    return render_template('users.html', players = players, Host = irgendeine_variable)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='81', debug=True)