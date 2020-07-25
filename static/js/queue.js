
var socket = io();

socket.on('game_found', function() {
    console.log("game found!");
});
