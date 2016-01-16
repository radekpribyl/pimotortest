from __future__ import print_function
from webapp import app, socketio
from flask_socketio import emit

ROBOT = app.config["ROBOT"]
steering = ROBOT.steering
dist_sensor = ROBOT.components["distance_sensor"]
obs_lf = ROBOT.components["obstacle_left"]
obs_rg = ROBOT.components["obstacle_right"]
connected_users = 0

steering_functions = {
    "dopredu" : steering.forward, "dozadu": steering.reverse,
    "rotujvlevo" : steering.spin_left, "rotujvpravo" : steering.spin_right,
    "zatocvpredvpravo" : steering.turn_right, "zatocvpredvlevo": steering.turn_left,
    "zatocvzadvlevo" : steering.turn_rev_left, "zatocvzadvpravo" : 
    steering.turn_rev_right, "stop": steering.stop}

 #Websockets
@socketio.on('connect', namespace='/malina')
def client_connect():
    global connected_users
    connected_users += 1
    if (connected_users > 0 and ROBOT.is_robot_initiated and not 
            dist_sensor.measure_running.is_set()):
        dist_sensor.start_distance_measure(lambda dist: socketio.emit('sensors',{'sensor':'distance', 'value':dist}, namespace='/malina'))
        obs_lf.register_both_callbacks(lambda pin, state: socketio.emit('sensors', {'sensor':'obs_lf', 'value':state}, namespace='/malina'))
        obs_rg.register_both_callbacks(lambda pin, state: socketio.emit('sensors', {'sensor':'obs_rg', 'value':state}, namespace='/malina'))
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
def io_rychlost(json):
    if json['akce'] == 'zrychli':
        speed = steering.increase_speed()
    if json['akce'] == 'zpomal':
        speed = steering.decrease_speed()
    
    emit('rychlost', {'rychlost' : speed}, broadcast=True)

@socketio.on('steering', namespace='/malina')
def io_steering(json):
    action = json['akce']
    if action in steering_functions:
        steering_functions[action]()
    else:
        print("Akce neni definovana: " + action)

@socketio.on_error('/malina')
def default_error_handler(e):
    print('An error has occurred: ' + str(e))
