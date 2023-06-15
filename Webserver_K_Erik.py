from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, session


app = Flask(__name__)
app.secret_key = 'sventegetscookie'
socketio = SocketIO(app)
online_users = []


@app.route('/indexErik')
def index():
    return render_template('indexErik.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    session['name'] = name
    #online_users.append(name)
    return render_template('submit.html')

@app.route('/display')
def display():
    name = session.get('name')
    return render_template('display.html', name=name)

@app.route('/users')
def users():
    return render_template('users.html')

@socketio.on('connect')
def handle_connect():
    name = session.get('name')
    online_users.append(name)
    emit('user_update', online_users, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    name = session.get('name')
    if name in online_users:
        online_users.remove(name)
    emit('user_update', online_users, broadcast=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='81', debug=True)