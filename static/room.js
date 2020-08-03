// Create WebSocket connection.

function appendChat(username, message) {
    if (username !== '') {
        $('#messages').append($('<li>').text(username + ': ' + message));
    } else {
        $('#messages').append($('<li>').text(message));
    }
}

class Room {
    constructor(username, room) {        
        this.socket = io();
        this.username = username;
        this.room = room;

        this.socket.on('connect', (data) => {
            this.socket.emit('join', {
                'username': this.username,
                'room': this.room
            });
        });

        this.socket.on('join', (data) => {
            console.log(data);
        });
    
        this.socket.on('set_state', (data) => {
            // TODO data['game']
            for (let chat of data['chat']) {
                console.log(chat)
                appendChat(chat['username'], chat['msg']);
            }
        })

        this.socket.on('chat', (data) => {
            appendChat(data['username'], data['msg']);
        });
    
    
        $('#chat').submit((event) => {
            event.preventDefault();
            
            this.socket.emit('chat', {
                'username': this.username,
                'msg': $('#chatInput').val(),
                'room': this.room
            });
            
            $('#chatInput').val('');
    
            return false;
        });
    }

}

