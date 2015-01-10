/// <reference file="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.0.min.js" />
/// <reference path="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.0-vsdoc.js" />

$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/malina');

    socket.on('rychlost', function (data) {
        console.log(data);
        $("#srychlost").html(data.rychlost);
    })

    socket.on('sensors', function (data) {
        console.log(data);
        $("#" + data.sensor).html(data.value);
    })

    $("#bdopredu").click(function () {
        socket.emit('motor', { akce: 'dopredu' });
    })
    $("#bstop").click(function () {
        socket.emit('motor', { akce: 'stop' });
    })

    $("#bdozadu").click(function () {
        socket.emit('motor', { akce: 'dozadu' });
    })

    $("#brotujedoleva").click(function () {
        socket.emit('motor', { akce: 'rotujvlevo' });
    })

    $("#brotujdoprava").click(function () {
        socket.emit('motor', { akce: 'rotujvpravo' });
    })

    $("#bvpredvlevo").click(function () {
        socket.emit('motor', { akce: 'zatocvpredvlevo' });
    })

    $("#bvredvpravo").click(function () {
        socket.emit('motor', { akce: 'zatocvpredvpravo' });
    })

    $("#bvzadvlevo").click(function () {
        socket.emit('motor', { akce: 'zatocvzadvlevo' });
    })

    $("#bvzadvpravo").click(function () {
        socket.emit('motor', { akce: 'zatocvzadvpravo' });
    })

    $("#bzrychli").click(function () {
        socket.emit('rychlost', { akce: 'zrychli' });
    })

    $("#bzpomal").click(function () {
        socket.emit('rychlost', { akce: 'zpomal' });
    })
})