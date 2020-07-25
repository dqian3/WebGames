from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}
rooms['test'] = []

# Templates
@app.route("/<room>")
def render_room(room):
    return render_template("room.html", room=room)


# Socket code
@socketio.on('connect')
def connect():
    send("")

@socketio.on('chat')
def chat(text):
    rooms['test'].append(chat)
    emit("chat", text)



if __name__ == '__main__':
    socketio.run(app)
