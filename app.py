from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit, join_room

from room import Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}
sessions = {}

# Templates/API for creating rooms
@app.route("/", methods=["GET"])
def render_index():
    return render_template("index.html")

@app.route("/create/<id>", methods=["POST"])
def create_room(id):
    if (id in rooms):
        return "Room {} already exists, try again".format(id), 409

    rooms[id] = Room(id)
    return "Created room {}".format(id), 200

@app.route("/<id>", methods=["GET"])
def render_room(id):
    if (id in rooms):
        return render_template("room.html", room=id)
    else:
        return render_template("404.html"), 404


# Socket code
def commit_chat(r_id, username, msg):
    room = rooms[r_id]

    chat = {
        'username': username,
        'msg': msg
    }

    room.chat.append(chat)
    socketio.emit("chat", chat, room=r_id)


@socketio.on('connect')
def connect():
    send("")

@socketio.on('disconnect')
def connect():
    if (request.sid not in sessions):
        return

    r_id = sessions[request.sid]
    username = rooms[r_id].session_disconnect(request.sid)    
    commit_chat(r_id, '', '{} disconnected!'.format(username))

@socketio.on('join')
def join(data):
    username = data['username']
    r_id = data['room']
    join_room(r_id)

    rooms[r_id].session_connect(username, request.sid)
    sessions[request.sid] = r_id

    # Catch up this user with state
    # TODO game state
    emit('set_state', {
        'chat': [chat for chat in rooms[r_id].chat]
    })

    # Emit to chat to notify others 
    commit_chat(r_id, '', '{} connected!'.format(username))

@socketio.on('chat')
def chat(data):
    username = data['username']
    r_id = data['room']
    chat = data['msg']

    commit_chat(r_id, username, chat)

@socketio.on('game')
def game(data):
    username = data['username']
    r_id = data['room']

    socketio.emit("game", data['msg'], room=r_id)


if __name__ == '__main__':
    socketio.run(app)
