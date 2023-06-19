import random
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
lobbies = {}
user_dic = {}



app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        hashed_password = hash_password(request.form.get('password'))
        if db_connection.check_login(username, hashed_password):
            session['username']=username
            user_dic.update(session)
            print(user_dic)
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

    if request.method == 'POST':

        if request.form['btn'] == 'Zufälligem Spiel beitreten':
            return redirect('/game_template')

        if request.form['btn'] == 'Spiel hosten':
            game_session_id = username + "_" + str(random.randint(100000,999999))
            lobbies[game_session_id] = {'players': []}
            session['game_session'] = game_session_id

            return redirect('/users')

        if request.form['btn'] == 'Spiel beitreten':
            return redirect('/lobby_list')

        # --- TEST IP ---
        if request.form['btn'] == 'Absenden':
            meineEingabe = request.form.get('meineEingabe')
            return redirect(f'/lobbies/{meineEingabe}')
        # --- ENDE TEST IP ---

    return render_template('startPage.html', username=username)

# --- TEST IP ---
@app.route('/lobbies/<meineEingabe>')
def lobbies(meineEingabe):
    return render_template('lobbies.html', meineEingabe=meineEingabe)
# --- ENDE TEST IP ---

@app.route('/game_template', methods=['GET', 'POST'])
def game():

    if request.method == 'POST':
        pass

    return render_template('game_template.html')

@app.route('/lobby_list', methods=['GET', 'POST'])
def lobby_list():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # Perform Python logic to calculate data
    data = {'x': 100, 'y': 200}  # Example data to send to the client
    return jsonify(data)


# -------- LOBBY TEST ---------
@app.route('/display', methods=['POST', 'GET'])
def display():

    game_session_id = session['game_session']

    if request.method == 'POST':
        return redirect('/users')

    username = session.get('username')
    return render_template('display.html', username=username, game_session_id=game_session_id)


@app.route('/users', methods=['POST', 'GET'])
def users():
    username = session.get('username')
    game_session = session['game_session']

    if request.method == 'POST':
        lobbies.pop(game_session)
        print(lobbies)
        return redirect('/startPage')

    return render_template('users.html', username=username, game_session=game_session)


@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    game_session = session['game_session']
    lobbies[game_session]['players'].append(username)
    print(lobbies)
    emit('user_update', lobbies[game_session]['players'], broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    game_session = session['game_session']
    if username in lobbies[game_session]['players']:
        lobbies[game_session]['players'].remove(username)
    print(lobbies)
    emit('user_update', lobbies[game_session]['players'], broadcast=True)


# ------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='81', debug=True)
