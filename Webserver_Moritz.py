from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Hier kannst du die empfangenen Daten verwenden
        print("Benutzername:", username)
        print("Passwort:", password)

        # Hier kannst du die gewünschte Logik basierend auf den Eingaben implementieren

        return render_template('startPage.html', username=username)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)

