var socket = io();

socket.on("connect", function () {
    socket.emit("connected");
});
socket.on("challenge", function (data) {
    console.log("challenge:");
    console.log(data);
});
socket.on("game_end", function(data) {
    console.log("game end:");
    console.log(data);
});

$(".ready-button").on("click", function() {
    socket.emit("ready");
    $(this).prop("disabled", true);
});
