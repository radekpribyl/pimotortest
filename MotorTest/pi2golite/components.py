"""
    Python Module including classes to control HW aspects of Pi2Go robot
    Provides access to basic functions of the Pi2Go robot
    No logic included in this module
    Module created by Radek Pribyl based on initial py2go file created 
    by Gareth Davies and Zachary Igielman
"""
#Import all modules/libraries
import time
import threading
import os
from pi2golite._helpers import validate_max

try:
    import RPi.GPIO as GPIO
except ImportError:
    import pi2golite.dummyGPIO as GPIO

#Set the mode here so that the classes can be possibly used without the
#Pi2Go.Robot class
GPIO.setmode(GPIO.BOARD)


#Classes
class Motor(object):
    def __init__(self, pin_fwd, pin_rev, correction=0):
        self._pin_fwd = pin_fwd
        self._pin_rev = pin_rev
        self._pwd_fwd = None
        self._pwd_rev = None
        self._correction = 1 - (float(validate_max(correction)) / 100)
        self._initialized = False

    def init(self, init_speed=20):
        if not self._initialized:
            init_speed = validate_max(init_speed)
            GPIO.setup(self._pin_fwd, GPIO.OUT)
            GPIO.setup(self._pin_rev, GPIO.OUT)
            self._pwd_fwd = GPIO.PWM(self._pin_fwd, init_speed)
            self._pwd_rev = GPIO.PWM(self._pin_rev, init_speed)
            self._pwd_fwd.start(0)
            self._pwd_rev.start(0)
            self._initialized = True

    def cleanup(self):
        if self._initialized:
            GPIO.cleanup(self._pin_fwd)
            GPIO.cleanup(self._pin_rev)
            self._initialized = False

    def forward(self, speed):
        if self._initialized:
            speed = validate_max(speed)
            self._pwd_fwd.ChangeFrequency(speed + 5)
            self._pwd_fwd.ChangeDutyCycle(speed * self._correction)
            self._pwd_rev.ChangeDutyCycle(0)

    def reverse(self, speed):
        if self._initialized:
            speed = validate_max(speed)
            self._pwd_rev.ChangeFrequency(speed + 5)
            self._pwd_rev.ChangeDutyCycle(speed * self._correction)
            self._pwd_fwd.ChangeDutyCycle(0)

    def stop(self):
        if self._initialized:
            self._pwd_rev.ChangeDutyCycle(0)
            self._pwd_fwd.ChangeDutyCycle(0)


class Sensor(object):
    def __init__(self, pin):
        self._pin = pin
        self._initialized = False

    def init(self):
        if not self._initialized:
            GPIO.setup(self._pin, GPIO.IN)
            self._initialized = True
                            
    def cleanup(self):
        if self._initialized:
            self.remove_callbacks()
            GPIO.cleanup(self._pin)
            self._initialized = False

    @property
    def activated(self):
        if self._initialized:
            if GPIO.input(self._pin) == 0:
                return True
            else:
                return False

    def _generate_callback(self, callback):
        def _call_callback(pin):
            state = self.activated
            callback(self._pin, state)
        return _call_callback

    def register_off_callback(self, callback):
        if self._initialized:
            fce_to_call = self._generate_callback(callback)
            GPIO.add_event_detect(self._pin, GPIO.RISING, callback=fce_to_call,
                                  bouncetime=100)

    def register_on_callback(self, callback):
        if self._initialized:
            fce_to_call = self._generate_callback(callback)
            GPIO.add_event_detect(self._pin, GPIO.FALLING, callback=fce_to_call,
                                  bouncetime=100)

    def register_both_callbacks(self, callback):
        if self._initialized:
            fce_to_call = self._generate_callback(callback)
            GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=fce_to_call,
                                  bouncetime=100)

    def remove_callbacks(self):
        if self._initialized:
            GPIO.remove_event_detect(self._pin)


class Switch(Sensor):
    def init(self):
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._initialized = True


class WheelSensor(object):
    """ The PINs for wheel sensors are shared with line detectors
    and need to be manually switched on the robot. Therefore the WheelSensor
    class needs configuration for line detector and delegates some of the
    method calls to it """

    def __init__(self, line_sensor):
        self._line_sensor = line_sensor

    def __getattr__(self, attrname):
        if attrname in (name for name in dir(self._line_sensor) if not name.startswith('_')):
            return getattr(self._line_sensor, attrname)
        else:
            raise AttributeError(attrname)


class WhiteLED(object):
    def __init__(self, pin):
        self._pin = pin
        self._pwm = None
        self._initialized = False

    def init(self):
        if not self._initialized:
            GPIO.setup(self._pin, GPIO.OUT)
            self._pwm = GPIO.PWM(self._pin, 100)
            self._pwm.start(0)
            self._initialized = True
                            
    def cleanup(self):
        if self._initialized:
            self.off()
            GPIO.cleanup(self._pin)
            self._initialized = False
    
    def on(self):
        self.set(100)

    def off(self):
        self.set(0)

    def set(self, intensity):
        if self._initialized:
            intensity = validate_max(100 - intensity)
            self._pwm.ChangeDutyCycle(intensity)

    def brighten(self, delay=0.1, step=5):
        for dc in range(0, 101, step):
            self.set(dc)
            time.sleep(delay)

    def dim(self, delay=0.1, step=5):
        for dc in range(100, -1, step * -1):
            self.set(dc)
            time.sleep(delay)


class DistanceSensor(object):
    def __init__(self, pin):
        self._pin = pin
        self.measure_running = threading.Event()
        self._measure_thread = None

    def init(self):
        pass

    def cleanup(self):
        if self.measure_running.is_set:
            self.stop_distance_measure()

    def _distance_measure(self, callback, delay=1):
        if delay < 0.2:
            delay = 0.2
        while self.measure_running.is_set():
            distance = self.get_distance()
            callback(distance)
            time.sleep(delay)
        GPIO.cleanup(self._pin)

    def start_distance_measure(self, callback, delay=1):
        if not self.measure_running.is_set():
            if callable(callback):
                self._measure_thread = threading.Thread(target=self._distance_measure,
                                                        args=(callback, delay))
                self.measure_running.set()
                self._measure_thread.start()
            else:
                raise AttributeError()

    def stop_distance_measure(self):
        if self.measure_running.is_set():
            self.measure_running.clear()

    def get_distance(self):
        GPIO.setup(self._pin, GPIO.OUT)
        # Send 10us pulse to trigger
        GPIO.output(self._pin, True)
        time.sleep(0.00001)
        GPIO.output(self._pin, False)

        GPIO.setup(self._pin, GPIO.IN)
        pulse_start = time.time()
        count = time.time()
        pulse_end = count
        while GPIO.input(self._pin) == 0 and time.time() - count < 0.1:
            pulse_start = time.time()

        count = time.time()
        while GPIO.input(self._pin) == 1 and time.time() - count < 0.1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return round(distance, 2)


class Servo(object):
    def __init__(self, pin, min_steps, max_steps, max_angle=180):
        self._pin = pin
        self._min_steps = min_steps
        self._max_steps = max_steps
        self._max_angle = max_angle
        self._curr_angle = 0
        self._initialized = False
        
    def set_angle(self, angle):
        if self._initialized:
            angle = validate_max(angle, self._max_angle)
            self._curr_angle = angle
            steps = int(self._min_steps + (self._curr_angle * (self._max_steps - self._min_steps) / self._max_angle))
            print(steps)
            os.system("echo P1-" + str(self._pin) + "=" + str(steps) + " > /dev/servoblaster") 

    def increase_angle(self, increment=10):
        self.set_angle(self._curr_angle + increment)
        return self._curr_angle

    def decrease_angle(self, decrement=10):
        self.set_angle(self._curr_angle - decrement)
        return self._curr_angle

    def init(self):
        self._initialized = True

    def cleanup(self):
        self._initialized = False

class ServosDriver(object):
    """Class which starts the servod blaster and configures it
    It also initiates servos which are connected (pan and tilt)"""
    idle_timeout = 2000
    min_steps = 50
    max_steps = 250
    def __init__(self, panpin=18, tiltpin=22):
        self._panpin = panpin
        self._tiltpin = tiltpin
        self.pan_servo = Servo(self._panpin, ServosDriver.min_steps, ServosDriver.max_steps)
        self.tilt_servo = Servo(self._tiltpin, ServosDriver.min_steps, ServosDriver.max_steps)
        self._initialized = False

    def init(self):
        """Starts the servod and initializes both servos"""
        if not self._initialized:
            path = os.path.split(os.path.realpath(__file__))[0]
            command = '/servod --idle-timeout=%s --min=%s --max=%s --p1pins="%s,%s" > /dev/null' % (ServosDriver.idle_timeout, ServosDriver.min_steps,
                                                ServosDriver.max_steps, self._panpin, self._tiltpin)
            print(command)
            os.system(path + command)
            self.pan_servo.init()
            self.tilt_servo.init()
            self._initialized = True

    def cleanup(self):
        """Stops the servod"""
        if self._initialized:
            self.pan_servo.cleanup()
            self.tilt_servo.cleanup()
            os.system('sudo killall servod')
            self._initialized = False
        