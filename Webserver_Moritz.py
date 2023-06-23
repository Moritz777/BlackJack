from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import emit
import db_connection
from Tools import hash_password
from player_class import Player
from user_class import User


app = Flask(__name__)
app.secret_key = 'sventegetscookie'
socketio = SocketIO(app)


users_dict={"open_lobbies":{}}

@app.route('/', methods=['GET', 'POST'])
def index():

    if 'username' not in session:
            return redirect('/login')

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        hashed_password = hash_password(request.form.get('password'))
        if db_connection.check_login(username, hashed_password):
            if username not in list(users_dict.keys()):
                if db_connection.check_blocked(username):
                    error_message = "Das Konto wurde gesperrt"
                    return render_template('index.html', error_message=error_message)
                if db_connection.check_admin(username):
                    return redirect('/admin')
                session['username'] = username
                users_dict[username] = {}
                # session['username'] = username
                return redirect('/startPage')
            return redirect('/registrierung')


        else:
            error_message = "Benutzername oder Passwort falsch"  # Fehlermeldung
            return render_template('index.html', error_message=error_message)
    else:
        return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    users_information = db_connection.get_all_players()
    if request.method == 'POST':
        username = request.form.get('searchInput')

        for element in users_information:
            if request.form['btn'] == f"{element[0]} blocken":
                db_connection.update_block_status(element[0], 'True')
                users_information = db_connection.get_all_players()
                error_message = element[0] + ' wurde geblockt.'
                return render_template('admin.html', users_information=users_information, error_message=error_message)

            if request.form['btn'] == f"{element[0]} entblocken":
                db_connection.update_block_status(element[0], 'False')
                users_information = db_connection.get_all_players()
                error_message = element[0] + ' wurde entblockt.'
                return render_template('admin.html', users_information=users_information, error_message=error_message)

        if request.form['btn']=='entblocken':
            db_connection.update_block_status(username, 'False')
            users_information = db_connection.get_all_players()
            error_message = username + ' wurde entblockt.'
            return render_template('admin.html', users_information=users_information, error_message=error_message)
        else:
            db_connection.update_block_status(username,'True')
            users_information = db_connection.get_all_players()
            error_message = username + ' wurde geblockt.'
            return render_template('admin.html', users_information=users_information, error_message=error_message)
    return render_template('admin.html', users_information=users_information)


@app.route('/registrierung', methods=['GET', 'POST'])
def registrierung():

    if request.method == 'POST':

        username = request.form.get('username')
        first_name = request.form.get('first_name')
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
            users_dict["open_lobbies"][username]=[]
            return redirect(f'/users/{username}')

        if request.form['btn'] == 'Spiel beitreten':
            return redirect('/lobby_list')

    return render_template('startPage.html', username=username, credit=users_dict[username].credit)


@app.route('/game_template/<host_name>', methods=['GET', 'POST'])
def game():

    if request.method == 'POST':
        pass

    return render_template('game_template.html')


@app.route('/users', methods=['POST', 'GET'])
def users():
    username = session.get('username')

    if request.method == 'POST':
        return redirect('/startPage')

    return render_template('users.html', username=username)


@app.route('/lobby_list', methods=['POST', 'GET'])
def lobbies():

    username = session.get('username')
    lobbies=users_dict["open_lobbies"].keys()
    lobbies=list(lobbies)

    if request.method == 'POST':

        for element in lobbies:
            if request.form['btn'] == f"{element} beitreten":
                return redirect(f'/users/{element}')
    return render_template('lobby_list.html', lobbies=lobbies)


@app.route('/users/<host_name>',methods=['POST', 'GET'])
def personal_lobby(host_name):

    if request.method == 'POST':

        if request.form['btn'] == 'Spiel starten':
            return render_template('game_template.html')
        if request.form['btn'] == 'Zurück zur Startseite':
            return redirect('/startPage')

    return render_template('game_template.html', Host = host_name)


#----------------------- SocketIO ----------------------------------------

@socketio.on('connect')
def handle_connect():
    # Verbindungsereignis behandeln
    username = session.get('username')
    host_name = request.referrer.split('/')[-1]
    users_dict["open_lobbies"][host_name].append(users_dict[username].username)
    users_list = users_dict['open_lobbies'][host_name]
    # users_list = []
    # for element in player_list:
    #     users_list.append(element)

    join_room(host_name)
    print(username, " connected to Lobby: ", host_name)
    print(users_dict["open_lobbies"])
    emit('user_update', users_list, room=host_name)

@socketio.on('disconnect')
def handle_disconnect():
    # Trennungsereignis behandeln
    username = session.get('username')
    host_name = request.referrer.split('/')[-1]

    users_dict["open_lobbies"][host_name].remove(username)
    users_list = users_dict["open_lobbies"][host_name]

    if username == host_name:
        del users_dict["open_lobbies"][host_name]

    leave_room(host_name)
    print(username, " disconnected from Lobby: ", host_name)
    print(users_dict["open_lobbies"])
    emit('user_update', users_list, room=host_name)

@socketio.on('startGameForEveryone')
def emit_game_start():
    print("hi to everyone")
    fiktive_karten = ["Herz", 4] # Hier könnten Karten übergeben werden
    emit('startSuccessFromPython', fiktive_karten, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug="True", host="0.0.0.0", port="81", debug="True")
