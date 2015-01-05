/// <reference file="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.0.min.js" />
/// <reference path="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.0-vsdoc.js" />

$(document).ready(function () {
    $("#bdopredu").click(function () {
        $.get("/motor/dopredu")
    })
    $("#bstop").click(function () {
        $.get("/motor/stop")
    })

    $("#bdozadu").click(function () {
        $.get("/motor/dozadu")
    })

    $("#brotujedoleva").click(function () {
        $.get("/motor/rotujvlevo")
    })

    $("#brotujdoprava").click(function () {
        $.get("/motor/rotujvpravo")
    })

    $("#bvpredvlevo").click(function () {
        $.get("/motor/zatocvpredvlevo")
    })

    $("#bvredvpravo").click(function () {
        $.get("/motor/zatocvpredvpravo")
    })

    $("#bvzadvlevo").click(function () {
        $.get("/motor/zatocvzadvlevo")
    })

    $("#bvzadvpravo").click(function () {
        $.get("/motor/zatocvzadvpravo")
    })

    $("#bzrychli").click(function () {
        $.get("/motor/zrychli", function( data ) {
            $("#srychlost").html(data.rychlost);
        })
    })

    $("#bzpomal").click(function () {
        $.get("/motor/zpomal", function( data ) {
            $("#srychlost").html(data.rychlost);
        })
    })
})