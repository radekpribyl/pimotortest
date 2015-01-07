from __future__ import print_function
from webapp import app, socketio
from flask import jsonify
from flask_socketio import emit
from json import loads


p = app.config["ROBOT"]
current_action = None
connected_users = 0

motor_functions = {
    "dopredu" : p.forward, "dozadu": p.reverse, "rotujvlevo" : p.spinLeft, "rotujvpravo" : p.spinRight,
    "zatocvpredvpravo" : p.turnForwardRight, "zatocvpredvlevo": p.turnForwardLeft, "zatocvzadvlevo" : p.turnReverseLeft,
    "zatocvzadvpravo" : p.turnReverseRight, "stop": p.stop}

#Helper functions
def provedAkci(action):
    if p.isRobotInitiated:
        action(p.currentSpeed)
        global current_action
        current_action = action

 #Websockets
@socketio.on('connect', namespace='/malina')
def client_connect():
    global connected_users
    connected_users += 1
    if connected_users == 1:
        print("Start background monitoring threads")
    print('New client connected: ' + str(connected_users))

@socketio.on('disconnect', namespace='/malina')
def client_disconnect():
    global connected_users
    connected_users -= 1
    if connected_users == 0:
        print("Stop all background threads")
    if connected_users < 0:
        connected_users = 0
    print('Client disconnected: ' + str(connected_users))

@socketio.on('rychlost', namespace='/malina')
def io_rychlost(json):
    if json['akce'] == 'zrychli':
        p.currentSpeed = p.currentSpeed + 10
    if json['akce'] == 'zpomal':
        p.currentSpeed = p.currentSpeed - 10
    if p.currentSpeed > 100 :
        p.currentSpeed = 100
    if p.currentSpeed < 1 :
        p.currentSpeed = 0
    if current_action is not None:
            current_action(p.currentSpeed)
    emit('rychlost' , {'rychlost' : p.currentSpeed}, broadcast=True)

@socketio.on('motor', namespace='/malina')
def io_motor(json):
    action = json['akce']
    if action in motor_functions:
        provedAkci(motor_functions[action])
    else:
        print("Akce neni definovana: " + action)

@socketio.on_error('/malina')
def default_error_handler(e):
    print('An error has occurred: ' + str(e))
