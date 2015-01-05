from webapp import app
from flask import jsonify

p=app.config["ROBOT"]
current_action = None

#Helper functions
def provedAkci(akce):
    if p.isRobotInitiated:
        akce(p.currentSpeed)
        global current_action
        current_action = akce

#Motor functions
@app.route('/motor/dopredu')
def dopredu():
    provedAkci(p.forward)
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
    provedAkci(p.reverse)
    return jsonify(response="ok")

@app.route('/motor/rotujvlevo')
def rotujvlevo():
    provedAkci(p.spinLeft)
    return jsonify(response="ok")

@app.route('/motor/rotujvpravo')
def rotujvpravo():
    provedAkci(p.spinRight)
    return jsonify(response="ok")


@app.route('/motor/zatocvpredvpravo')
def zatocvpredvpravo():
    provedAkci(p.turnForwardRight)
    return jsonify(response="ok")

@app.route('/motor/zatocvpredvlevo')
def zatocvpredvlevo():
    provedAkci(p.turnForwardLeft)
    return jsonify(response="ok")

@app.route('/motor/zatocvzadvlevo')
def zatocvzadvlevo():
    provedAkci(p.turnReverseLeft)
    return jsonify(response="ok")

@app.route('/motor/zatocvzadvpravo')
def zatocvzadvpravo():
    provedAkci(p.turnReverseRight)
    return jsonify(response="ok")

@app.route('/motor/zrychli')
def zrychli():
    if p.isRobotInitiated:
        p.currentSpeed = p.currentSpeed + 10
        if p.currentSpeed > 100 :
            p.currentSpeed = 100
        if current_action is not None:
            current_action(p.currentSpeed)
    return jsonify(response="ok", rychlost=p.currentSpeed)

@app.route('/motor/zpomal')
def zpomal():
    if p.isRobotInitiated:
        p.currentSpeed = p.currentSpeed - 10
        if p.currentSpeed < 1 :
            p.currentSpeed = 0
        if current_action is not None:
            current_action(p.currentSpeed)
    return jsonify(response="ok", rychlost=p.currentSpeed)