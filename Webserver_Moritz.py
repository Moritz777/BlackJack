from flask import Flask, render_template, request, redirect
import db_connection
from Tools import hash_password
from user_class import User

# from create_new_user_on_registry import new_user

# import create_new_user_on_registry


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        username = request.form.get('username')
        hashed_password = hash_password(request.form.get('password'))

        if db_connection.check_login(username,hashed_password):
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
        new_user = User(username, hashed_password)
        if db_connection.check_login(username,hashed_password):
            error_message = "Benutzernamen bereits vergeben"  # Fehlermeldung
            return render_template('regestrierung.html', error_message=error_message)

        else:
            return render_template('startPage.html', username="Benutzer wurde angelegt")
    else:
        return render_template('regestrierung.html')

if __name__ == "__main__":
    app.run(host='localhost', port='81', debug=True)

