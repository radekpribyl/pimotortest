from __future__ import print_function
from webapp import app, socketio
from flask import jsonify
from flask_socketio import emit
from json import loads
import atexit

robot = app.config["ROBOT"]
motor = robot.motor
dist_sensor = robot.distance_sensor
obs_lf = robot.obstacle_left
obs_rg = robot.obstacle_right
connected_users = 0

motor_functions = {
    "dopredu" : motor.forward, "dozadu": motor.reverse, "rotujvlevo" : motor.spin_left,
    "rotujvpravo" : motor.spin_right, "zatocvpredvpravo" : motor.turn_forward_right,
    "zatocvpredvlevo": motor.turn_forward_left, "zatocvzadvlevo" : motor.turn_reverse_left,
    "zatocvzadvpravo" : motor.turn_reverse_right, "stop": motor.stop}

#Helper functions
@atexit.register
def teardown_print():
    robot.cleanup()

 #Websockets
@socketio.on('connect', namespace='/malina')
def client_connect():
    global connected_users
    connected_users += 1
    if connected_users > 0 and robot.is_robot_initiated and not dist_sensor.measure_running.is_set():
        dist_sensor.start_distance_measure(lambda(dist): socketio.emit('sensors',
                                           {'sensor':'distance', 'value':dist}, namespace='/malina'))
        obs_lf.register_both_callbacks(lambda(pin, state): socketio.emit('sensors',
                                           {'sensor':'obs_lf', 'value':state}, namespace='/malina'))
        obs_rg.register_both_callbacks(lambda(pin, state): socketio.emit('sensors',
                                           {'sensor':'obs_rg', 'value':state}, namespace='/malina'))
    print('New client connected: ' + str(connected_users))

@socketio.on('disconnect', namespace='/malina')
def client_disconnect():
    global connected_users
    connected_users -= 1
    if connected_users == 0:
        dist_sensor.stop_distance_measure()
        obs_lf.remove_callbacks()
        obs_rg.remove_callbacks()
    if connected_users < 0:
        connected_users = 0
    print('Client disconnected: ' + str(connected_users))

@socketio.on('rychlost', namespace='/malina')
def io_rychlost( json ):
    if json['akce'] == 'zrychli':
        speed = motor.increase_speed()
    if json['akce'] == 'zpomal':
        speed = motor.decrease_speed()
    
    emit('rychlost' , {'rychlost' : speed}, broadcast=True)

@socketio.on('motor', namespace='/malina')
def io_motor( json ):
    action = json['akce']
    if action in motor_functions:
        motor_functions[action]()
    else:
        print("Akce neni definovana: " + action)

@socketio.on_error('/malina')
def default_error_handler( e ):
    print('An error has occurred: ' + str(e))
