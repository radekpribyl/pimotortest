from webapp import app

from flask import render_template, url_for, redirect, jsonify

import pi2go as p

#, request, jsonify, abort, make_response, url_for, redirect

zapnuty = False
rychlost = 30
current_action = None

@app.route('/')
def home():
    return render_template('Index.html', zapnuty = zapnuty)

@app.route('/prepni')
def prepni():
    global zapnuty
    if zapnuty:
        p.cleanup()
    else:
        p.init()
    zapnuty = not zapnuty
    return redirect(url_for('home'))

#Motor functions
@app.route('/motor/dopredu')
def dopredu():
    if zapnuty:
        p.forward(rychlost)
        global current_action
        current_action = p.forward
    return jsonify(response="ok")

@app.route('/motor/stop')
def stop():
    if zapnuty:
        p.stop()
        global current_action
        current_action = None
    return jsonify(response="ok")

@app.route('/motor/dozadu')
def dozadu():
    if zapnuty:
        p.reverse(rychlost)
        global current_action
        current_action = p.reverse
    return jsonify(response="ok")

@app.route('/motor/zrychli')
def zrychli():
    if zapnuty:
        rychlost = rychlost + 10
        if rychlost > 100 :
            rychlost = 100
        if current_action is not None:
            current_action(rychlost)
    return jsonify(response="ok")

@app.route('/motor/zpomal')
def zpomal():
    if zapnuty:
        rychlost = rychlost - 10
        if rychlost < 1 :
            rychlost = 0
        if current_action is not None:
            current_action(rychlost)
    return jsonify(response="ok")