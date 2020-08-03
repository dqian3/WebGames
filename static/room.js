// Create WebSocket connection.
function init(roomId) {
    let socket = io();
    
    socket.on("join", (msg) => {
        console.log(msg);
    });

    socket.on("chat", (msg) => {
        $('#messages').append($('<li>').text(msg));
    });


    $('#chat').submit(function (e) {
        e.preventDefault();
        
        socket.emit('chat', {
            'chat': $('#chatInput').val(),
            'room': roomId
        });
        
        $('#chatInput').val('');

        return false;
    });
};

