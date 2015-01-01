﻿/// <reference file="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.0.min.js" />
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

    $("#bzrychli").click(function () {
        $.get("/motor/zrychli")
    })

    $("#bzpomal").click(function () {
        $.get("/motor/zpomal")
    })
})