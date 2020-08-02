// Create WebSocket connection.
function init (room_id) {
    var socket = io();

    $('form').submit(function (e) {
        e.preventDefault();
        socket.emit('chat', $('#m').val());
        $('#m').val('');
        return false;
    });
    
    socket.on("chat", (msg) => {
        $('#messages').append($('<li>').text(msg));
    });


};

