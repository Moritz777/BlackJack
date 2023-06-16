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
online_users = []

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
        last_username = request.form.get('last_name')
        birthday = request.form.get('birthdaytime')
        today = datetime.now()
        birthday_object = datetime.fromisoformat(birthday)
        age = (today.day - birthday_object.day) / 365
        if age < 18:
            return render_template('registrierung.html',
                                   error_message="Regestrierung fehlgeschlagen,das Mindestalter ist 18 Jahre")
        hashed_password = hash_password(request.form.get('password'))

        if db_connection.check_username(username):
            return render_template('registrierung.html', error_message="Der Username ist bereits vergeben")
        else:
            new_user = User(username, hashed_password)
            flash("Registrierung erfolgreich, bitte melden Sie sich an")
            return redirect("/")

    return render_template('registrierung.html')


@app.route('/startPage', methods=['GET', 'POST'])
def random_session():
    if request.method == 'POST':

        if request.form['btn'] == 'Zufälligem Spiel beitreten':
            return redirect('/game_template')

        if request.form['btn'] == 'Spiel hosten':
            return redirect('/display')

        if request.form['btn'] == 'Spiel beitreten':
            return redirect('/lobby_list')

    username = session['username']
    return render_template('startPage.html', username=username)


@app.route('/game_template', methods=['GET', 'POST'])
def game():
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

    if request.method == 'POST':
        return redirect('/users')

    username = session.get('username')
    return render_template('display.html', username=username)


@app.route('/users', methods=['POST', 'GET'])
def users():

    if request.method == 'POST':
        return redirect('/display')

    username = session.get('username')
    return render_template('users.html', username=username)


@socketio.on('connect')
def handle_connect():
    username = session.get('username')
    online_users.append(username)
    emit('user_update', online_users, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in online_users:
        online_users.remove(username)
    emit('user_update', online_users, broadcast=True)


# ------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='81', debug=True)
