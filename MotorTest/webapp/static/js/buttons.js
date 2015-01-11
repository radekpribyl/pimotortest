/// <reference file="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.0.min.js" />
/// <reference path="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.0-vsdoc.js" />

$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/malina');

    socket.on('rychlost', function (data) {
        $("#srychlost").html(data.rychlost);
    })

    socket.on('sensors', function (data) {
        $("#" + data.sensor).html(data.value);
    })

    $("#bdopredu").click(function () {
        socket.emit('steering', { akce: 'dopredu' });
    })
    $("#bstop").click(function () {
        socket.emit('steering', { akce: 'stop' });
    })

    $("#bdozadu").click(function () {
        socket.emit('steering', { akce: 'dozadu' });
    })

    $("#brotujedoleva").click(function () {
        socket.emit('steering', { akce: 'rotujvlevo' });
    })

    $("#brotujdoprava").click(function () {
        socket.emit('steering', { akce: 'rotujvpravo' });
    })

    $("#bvpredvlevo").click(function () {
        socket.emit('steering', { akce: 'zatocvpredvlevo' });
    })

    $("#bvredvpravo").click(function () {
        socket.emit('steering', { akce: 'zatocvpredvpravo' });
    })

    $("#bvzadvlevo").click(function () {
        socket.emit('steering', { akce: 'zatocvzadvlevo' });
    })

    $("#bvzadvpravo").click(function () {
        socket.emit('steering', { akce: 'zatocvzadvpravo' });
    })

    $("#bzrychli").click(function () {
        socket.emit('rychlost', { akce: 'zrychli' });
    })

    $("#bzpomal").click(function () {
        socket.emit('rychlost', { akce: 'zpomal' });
    })
})