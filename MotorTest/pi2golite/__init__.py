from pi2golite.components import DistanceSensor, Motor, Sensor, Switch, WhiteLED, WheelSensor, ServosDriver
from pi2golite.behaviours import Steering

class Robot(object):
    """The Robot class assebles all the individual components together
    and adds basic behaviours to the pi2golite robot"""

    def __init__(self, wheel_sensors=True, servos=True):
        self.is_robot_initiated = False

        #Defining robot's hardware components
        self.components = {}
        
        #Both motor setup
        left_motor = Motor(26, 24, 7.3)
        right_motor = Motor(19, 21)
        self.components['left_motor'] = left_motor
        self.components['right_motor'] = right_motor

        #While LEDs setup
        self.components['front_Led'] = WhiteLED(15)
        self.components['rear_Led'] = WhiteLED(16)

        #IR sensors
        self.components['obstacle_left'] = Sensor(7)
        self.components['obstacle_right'] = Sensor(11)
        self.components['linesensor_left'] = Sensor(12)
        self.components['linesensor_right'] = Sensor(13)

        #Switch
        self.components['switch'] = Switch(23)

        #Distance sensor
        self.components['distance_sensor'] = DistanceSensor(8)

        #Optional components
        #Aliases for wheel sensors as they have to be switched
        #Pins are the same as for line sensors
        if wheel_sensors:
            self.components['wheelsensor_left'] = WheelSensor(self.components['linesensor_left'])
            self.components['wheelsensor_right'] = WheelSensor(self.components['linesensor_right'])

        #Servos
        if servos:
            self.components['servos'] = ServosDriver()

        #Adding behaviour
        self.steering = Steering(left_motor, right_motor)

    def __getattr__(self, attrname):
        """"Delegate to steering instance to simplify access to key robot's methods"""
        if attrname in (name for name in dir(self.steering) if not name.startswith('_')):
            return getattr(self.steering, attrname)
        else:
            raise AttributeError(attrname)

    def init(self):
        """Initialize all components connected to pi2golite robot"""
        for component in self.components.values():
            component.init()
        self.is_robot_initiated = True

    def cleanup(self):
        """Clean all components."""
        for component in self.components.values():
            component.cleanup()
        self.is_robot_initiated = False
