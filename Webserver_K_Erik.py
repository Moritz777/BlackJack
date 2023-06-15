from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'sventegetscookie'


@app.route('/indexErik')
def index():
    return render_template('indexErik.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    session['name'] = name
    # return render_template('display.html')
    return 'OK'

@app.route('/display')
def display():
    name = session.get('name')
    return render_template('display.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='81', debug=True)