from __future__ import print_function
from webapp import app, socketio
from flask import jsonify
from flask_socketio import emit
from json import loads
import atexit

robot = app.config["ROBOT"]
steering = robot.steering
dist_sensor = robot.distance_sensor
obs_lf = robot.obstacle_left
obs_rg = robot.obstacle_right
connected_users = 0

steering_functions = {
    "dopredu" : steering.forward, "dozadu": steering.reverse, "rotujvlevo" : steering.spin_left,
    "rotujvpravo" : steering.spin_right, "zatocvpredvpravo" : steering.turn_forward_right,
    "zatocvpredvlevo": steering.turn_forward_left, "zatocvzadvlevo" : steering.turn_reverse_left,
    "zatocvzadvpravo" : steering.turn_reverse_right, "stop": steering.stop}

 #Websockets
@socketio.on('connect', namespace='/malina')
def client_connect():
    global connected_users
    connected_users += 1
    if connected_users > 0 and robot.is_robot_initiated and not dist_sensor.measure_running.is_set():
        dist_sensor.start_distance_measure(lambda dist: socketio.emit('sensors',
                                           {'sensor':'distance', 'value':dist}, namespace='/malina'))
        obs_lf.register_both_callbacks(lambda pin, state: socketio.emit('sensors',
                                           {'sensor':'obs_lf', 'value':state}, namespace='/malina'))
        obs_rg.register_both_callbacks(lambda pin, state: socketio.emit('sensors',
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
        speed = steering.increase_speed()
    if json['akce'] == 'zpomal':
        speed = steering.decrease_speed()
    
    emit('rychlost' , {'rychlost' : speed}, broadcast=True)

@socketio.on('steering', namespace='/malina')
def io_steering( json ):
    action = json['akce']
    if action in steering_functions:
        steering_functions[action]()
    else:
        print("Akce neni definovana: " + action)

@socketio.on_error('/malina')
def default_error_handler( e ):
    print('An error has occurred: ' + str(e))
