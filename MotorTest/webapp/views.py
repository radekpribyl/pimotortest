from webapp import app

from flask import render_template, url_for, redirect, jsonify

#import pi2go as p
#import pi2gomock as p
robot = app.config["ROBOT"]

#, request, jsonify, abort, make_response, url_for, redirect
@app.route('/')
def home():
    config = {"zapnuty" : robot.is_robot_initiated, "rychlost" : robot.steering.current_speed}
    return render_template('Index.html', config = config)

@app.route('/prepni')
def prepni():
    if robot.is_robot_initiated:
        robot.cleanup()
    else:
        robot.init()
    return redirect(url_for('home'))