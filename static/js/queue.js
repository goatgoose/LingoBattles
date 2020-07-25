var socket = io();

socket.on("connect", function () {
    socket.emit("connected");
});
socket.on("game_found", function (data) {
    console.log("game found!");
    window.location.replace("/game/" + data.id);
});
