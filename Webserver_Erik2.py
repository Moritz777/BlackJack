import random
from datetime import date, datetime

import socketio
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import emit

import db_connection
from Tools import hash_password
from db_connection import get_credit
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
users_dict= {"open_lobbies": {}}
lobbies_test = {}

app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages


@app.route('/', methods=['GET', 'POST'])
def index():

    # if 'username' not in session:
    #     print("Browsersession existiert schon") klappt nicht

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

@app.route('/game_template', methods=['GET', 'POST'])
def game():

    username = session.get('username')
    if request.method == 'POST':
        pass

    return render_template('game_template.html')


@app.route('/users', methods=['POST', 'GET'])
def users():
    username = session.get('username')

    if request.method == 'POST':
        return redirect('/startPage')

    return render_template('users.html', username=username)


@app.route('/startPage', methods=['GET', 'POST'])
def random_session():

    username = session.get('username')
    users_dict[username] = Player(username)

    if request.method == 'POST':

        if request.form['btn'] == 'Zufälligem Spiel beitreten':
            return redirect('/game_template')

        if request.form['btn'] == 'Spiel hosten':
            #users_dict["open_lobbies"][username]=[Player(username)]
            lobbies_test[username] = [username]
            print(lobbies_test)
            return redirect(f'/users/{username}')

        if request.form['btn'] == 'Spiel beitreten':
            return redirect('/lobby_list')

    return render_template('startPage.html', username=username, credit=users_dict[username].credit)

@app.route('/lobby_list', methods=['POST', 'GET'])
def lobbies():

    username = session.get('username')
    # lobbies=users_dict["open_lobbies"].keys()
    lobbies = lobbies_test.keys()
    lobbies=list(lobbies)

    if request.method == 'POST':

        # for element in lobbies:
        for element in lobbies:
            if request.form['btn'] == f"{element} beitreten":
                #users_dict["open_lobbies"][element].append(users_dict[username])
                lobbies_test[element].append(username)
                return redirect(f'/users/{element}')
    return render_template('lobby_list.html', lobbies=lobbies)



@app.route('/users/<hostname>')
def personal_lobby(hostname):

    username = session.get('username')
    print(hostname)
    #if hostname not in lobbies_test:    # Der Host erstellt und fügt sich hinzu
        #lobbies_test[hostname] = [hostname]
        #print(lobbies_test)
    #else:
       # lobbies_test[hostname].append(username)
        #print(lobbies_test)
    # onlineUsersList = users_dict["open_lobbies"][irgendeine_variable]

    # @socketio.on('connect')
    # def handle_connect():
    #     onlineUsersList.append(users_dict["open_lobbies"][irgendeine_variable])

    # emit('user_update', broadcast=True)

    # print(irgendeine_variable)
    #
    # players = []
    #
    # print(users_dict)
    #
    # for element in users_dict["open_lobbies"][irgendeine_variable]:
    #     players.append(element.username)
    #
    # print(players)

    current_players = []
    for curr_player in lobbies_test[hostname]:
        current_players.append(curr_player)

    return render_template('users.html', current_players=current_players, hostname=hostname)


@socketio.on('connect')
def handle_connect():
    # Verbindungsereignis behandeln
    username = session.get('username')
    print(username + 'connected')

@socketio.on('disconnect')
def handle_disconnect():
    # Trennungsereignis behandeln
    username = session.get('username')
    hostname = request.referrer.split('//')[-1].split('/')[-1]
    print('Disconnected from: ', hostname)
    print(username + 'disconnected')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='81', debug=True)