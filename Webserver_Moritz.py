import random
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, redirect, url_for, flash
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
# socketio = SocketIO(app)
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


@app.route('/startPage', methods=['GET', 'POST'])
def random_session():

    username = session['username']
    users_dict[username] = Player(username)

    if request.method == 'POST':

        if request.form['btn'] == 'Zufälligem Spiel beitreten':
            return redirect('/game_template')

        if request.form['btn'] == 'Spiel hosten':
            users_dict["open_lobbies"][username]={"Player_1":users_dict[username]}
            print(users_dict)
            return redirect(f'/users/{username}')

        if request.form['btn'] == 'Spiel beitreten':
            return redirect('/lobby_list')

    return render_template('startPage.html', username=username, credit=users_dict[username].credit)


@app.route('/game_template', methods=['GET', 'POST'])
def game():

    if request.method == 'POST':
        pass

    return render_template('game_template.html')

@app.route('/api/data')
def get_data():
    # Perform Python logic to calculate data
    data = {'x': 100, 'y': 200}  # Example data to send to the client
    return jsonify(data)



@app.route('/users', methods=['POST', 'GET'])
def users():
    username = session.get('username')
    print(users_dict["open_lobbies"][username])

    if request.method == 'POST':
        return redirect('/startPage')

    return render_template('users.html', username=username)

@app.route('/lobby_list', methods=['POST', 'GET'])
def lobbies():
    username = session.get('username')
    lobbies=users_dict["open_lobbies"].keys()
    lobbies=list(lobbies)

    print(lobbies)

    if request.method == 'POST':

        print("post methode")

        for element in lobbies:
            if request.form['btn'] == f"{element} beitreten":
                print(element)
                return redirect(f'/users/{element}')
    return render_template('lobby_list.html', lobbies=lobbies)

@app.route('/users/<irgendeine_variable>')
def personal_lobby(irgendeine_variable):
    return render_template('users.html', irgendeine_variable=irgendeine_variable)







#
# @socketio.on('connect')
# def handle_connect():
#     username = session.get('username')
#     game_session = lobbies
#     lobbies[game_session]['players'].append(username)
#     print(lobbies)
#     emit('user_update', broadcast=True)
#
#
# @socketio.on('disconnect')
# def handle_disconnect():
#     username = session.get('username')
#     game_session = session['game_session']
#     if username in lobbies[game_session]['players']:
#         lobbies[game_session]['players'].remove(username)
#     print(lobbies)
#     emit('user_update', lobbies[game_session]['players'], broadcast=True)


# ------------------------

if __name__ == "__main__":
    app.run(host='localhost', port='81', debug=True)
