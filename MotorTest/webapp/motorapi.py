from webapp import app
from flask import jsonify

p=app.config["ROBOT"]
current_action = None

#Motor functions
@app.route('/motor/dopredu')
def dopredu():
    if p.isRobotInitiated:
        p.forward(p.currentSpeed)
        global current_action
        current_action = p.forward
    return jsonify(response="ok")

@app.route('/motor/stop')
def stop():
    if p.isRobotInitiated:
        p.stop()
        global current_action
        current_action = None
    return jsonify(response="ok")

@app.route('/motor/dozadu')
def dozadu():
    if p.isRobotInitiated:
        p.reverse(p.currentSpeed)
        global current_action
        current_action = p.reverse
    return jsonify(response="ok")

@app.route('/motor/zrychli')
def zrychli():
    if p.isRobotInitiated:
        p.currentSpeed = p.currentSpeed + 10
        if p.currentSpeed > 100 :
            p.currentSpeed = 100
        print "current action is: %s" % (current_action)
        if current_action is not None:
            print "calling %s %s" % (current_action, p.currentSpeed)
            current_action(p.currentSpeed)
    return jsonify(response="ok", rychlost=p.currentSpeed)

@app.route('/motor/zpomal')
def zpomal():
    if p.isRobotInitiated:
        p.currentSpeed = p.currentSpeed - 10
        if p.currentSpeed < 1 :
            p.currentSpeed = 0
        print "current action is: %s" % (current_action)
        if current_action is not None:
            print "calling %s %s" % (current_action, p.currentSpeed)
            current_action(p.currentSpeed)
    return jsonify(response="ok", rychlost=p.currentSpeed)