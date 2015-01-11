from components import DistanceSensor, Motor, Sensor, Switch, WhiteLED
from behaviours import Steering

class Robot(object):
    def __init__( self ):
        self._components = []
        self.is_robot_initiated = False
        #Both motor setup
        left_motor = Motor(26, 24, 7.3)
        right_motor = Motor(19, 21)
        self._components.append(left_motor)
        self._components.append(right_motor)
        self.steering = Steering(left_motor, right_motor)

        #While LEDs setup
        self.front_LED = WhiteLED(15)
        self.rear_LED = WhiteLED(16)
        self._components.append(self.front_LED)
        self._components.append(self.rear_LED)

        #IR sensors
        self.obstacle_left = Sensor(7)
        self.obstacle_right = Sensor(11)
        self.linesensor_left = Sensor(12)
        self.linesensor_right = Sensor(13)
        self._components.append(self.obstacle_left)
        self._components.append(self.obstacle_right)
        self._components.append(self.linesensor_left)
        self._components.append(self.linesensor_right)

        #Aliases for wheel sensors as they have to be switched
        #Pins are the same as for line sensors
        self.wheelsensor_left = self.linesensor_left
        self.wheelsensor_right = self.linesensor_right

        #Switch
        self.switch = Switch(23)
        self._components.append(self.switch)

        #Distance sensor
        self.distance_sensor = DistanceSensor(8)
        self._components.append(self.distance_sensor)

    def init( self ):
        for component in self._components:
            component.init()
        self.is_robot_initiated = True

    def cleanup( self ):
        for component in self._components:
            component.cleanup()
        self.is_robot_initiated = False