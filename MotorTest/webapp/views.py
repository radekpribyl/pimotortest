from webapp import app

from flask import render_template

import pi2go as p

#, request, jsonify, abort, make_response, url_for, redirect

zapnuty = False
rychlost = 30

@app.route('/')
def home():
    return render_template('index.html', zapnuty = zapnuty)

@app.route('/prepni')
def prepni():
    global zapnuty
    if zapnuty:
        p.cleanup()
    else:
        p.init()
    zapnuty = not zapnuty
    return redirect(url_for('home'))

@app.route('/dopredu')
def dopredu():
    if zapnuty:
        p.forward(rychlost)
    return redirect(url_for('home'))

@app.route('/stop')
def stop():
    if zapnuty:
        p.stop()
    return redirect(url_for('home'))
