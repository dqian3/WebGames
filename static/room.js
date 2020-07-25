// Create WebSocket connection.
function init (room_id) {
    var socket = io();

    $('form').submit(function (e) {
        e.preventDefault(); // prevents page reloading
        console.log( $('#m').val());
        socket.emit('chat', $('#m').val());
        $('#m').val('');
        return false;
    });
    
    socket.on("chat", (msg) => {
        console.log("chat received");
        console.log(msg);
        $('#messages').append($('<li>').text(msg));
    });

};

