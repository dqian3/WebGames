from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room

from room import Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}

# Templates/API for creating rooms
@app.route("/", methods=["GET"])
def render_index():
    return render_template("index.html")

@app.route("/create/<id>", methods=["POST"])
def create_room(id):
    rooms[id] = Room(id)
    return "Created room {}".format(id), 200

@app.route("/<id>", methods=["GET"])
def render_room(id):
    if (id in rooms):
        return render_template("room.html", room=id)
    else:
        return render_template("404.html"), 404


# Socket code
@socketio.on('connect')
def connect():
    send("")

@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)
    send("Joined!")

@socketio.on('chat')
def chat(data):
    room = data['room']
    chat = data['chat']
    emit("chat", chat, room=room)

if __name__ == '__main__':
    socketio.run(app)
