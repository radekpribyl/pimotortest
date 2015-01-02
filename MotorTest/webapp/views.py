from webapp import app

from flask import render_template, url_for, redirect, jsonify

#import pi2go as p
#import pi2gomock as p
p=app.config["ROBOT"]

#, request, jsonify, abort, make_response, url_for, redirect

@app.route('/')
def home():
    config = {"zapnuty" : p.isRobotInitiated, "rychlost" : p.currentSpeed}
    return render_template('Index.html', config = config)

@app.route('/prepni')
def prepni():
    if p.isRobotInitiated:
        p.cleanup()
    else:
        p.init()
    p.isRobotInitiated = not p.isRobotInitiated
    return redirect(url_for('home'))