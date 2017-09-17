from webapp import app
from flask import render_template, url_for, redirect

ROBOT = app.config["ROBOT"]

@app.route('/')
def home():
    config = {"zapnuty" : ROBOT.is_robot_initiated,
              "rychlost" : ROBOT.steering.current_speed}

    return render_template('Index.html', config=config)

@app.route('/prepni')
def prepni():
    if ROBOT.is_robot_initiated:
        ROBOT.cleanup()
    else:
        ROBOT.init()
    return redirect(url_for('home'))
