from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Hier können Sie die POST-Daten verarbeiten
        username = request.form.get('username')
        password = request.form.get('password')


        return "Danke für Ihre Anmeldung!"

a = 5

if __name__ == "__main__":
    app.run(host="10.130.240.91", port=80, debug=True)
