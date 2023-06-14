from flask import Flask, render_template, request, redirect
import db_connection
from Tools import hash_password
from player_class import Player
from user_class import User
from Control import control

# from create_new_user_on_registry import new_user

# import create_new_user_on_registry

players = []
app = Flask(__name__)

control = control()
player = Player

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        username = request.form.get('username')
        hashed_password = hash_password(request.form.get('password'))

        if db_connection.check_login(username,hashed_password):
           player = control.create_new_player(username)
           return render_template('startPage.html', username=username)
        else:
            error_message = "Benutzer nicht vorhanden"  # Fehlermeldung
            return render_template('index.html', error_message=error_message)


    else:
        return render_template('index.html')


@app.route('/registrierung', methods=['GET', 'POST'])
def registrierung():
    if request.method == 'POST':
        username = request.form.get('username')
        hashed_password = hash_password(request.form.get('password'))
        if db_connection.check_username(username):
            error_message = "Benutzernamen bereits vergeben"  # Fehlermeldung
            return render_template('regestrierung.html', error_message=error_message)

        else:
            new_user = User(username, hashed_password)
            return render_template('index.html',message="Regestrierung erfolgreich, bitte melden Sie sich an")
    return render_template('regestrierung.html')

@app.route('/startPage', methods=['GET', 'POST'])
def random_session():
    if request.method == 'POST':
        control.choose_session(player)
        print(control.session_list[-1].player_list)
    return render_template('game_template.html')


@app.route('/game_template', methods=['GET', 'POST'])
def game():
    return render_template('game_template.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='81', debug=True)

