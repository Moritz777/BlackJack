from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Hier kannst du die empfangenen Daten verwenden
        print("Benutzername:", username)
        print("Passwort:", password)

        user_name = False

        if user_name:
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
        password = request.form.get('password')

        return redirect('/')
    else:
        return render_template('regestrierung.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='81', debug=True)

