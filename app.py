from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Store messages in memory (for simplicity)
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Send previous messages to the new user
    for msg in messages:
        emit('message', msg)

@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    messages.append(msg)
    send(msg, broadcast=True)

@socketio.on('clear')
def handle_clear():
    global messages
    messages = []
    emit('clear', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
