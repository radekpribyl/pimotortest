# Python Module to control HW aspects of Pi2Go robot
# Provides access to basic functions of the Pi2Go robot
# No logic included in this module

#Import all modules/libraries
import time
import threading
from _helpers import validate_max100

try:
    import RPi.GPIO as GPIO
except ImportError:
    import dummyGPIO as GPIO

#Set the mode here so that the classes can be possibly used without the
#Pi2GoRobot class
GPIO.setmode(GPIO.BOARD)


#Classes
class Motor(object):
    def __init__( self,pin_fwd, pin_rev, correction = 0 ):
        self._pin_fwd = pin_fwd
        self._pin_rev = pin_rev
        self._correction = 1 - (float(validate_max100(correction)) / 100)
        self._initialized = False

    def init( self, init_speed = 20 ):
        if not self._initialized:
            init_speed = validate_max100(init_speed)
            GPIO.setup(self._pin_fwd, GPIO.OUT)
            GPIO.setup(self._pin_rev, GPIO.OUT)
            self._pwd_fwd = GPIO.PWM(self._pin_fwd, init_speed)
            self._pwd_rev = GPIO.PWM(self._pin_rev, init_speed)
            self._pwd_fwd.start(0)
            self._pwd_rev.start(0)
            self._initialized = True

    def cleanup( self ):
        GPIO.cleanup(self._pin_fwd)
        GPIO.cleanup(self._pin_rev)
        self._initialized = False

    def forward( self, speed ):
        if self._initialized:
            speed = validate_max100(speed)
            self._pwd_fwd.ChangeFrequency(speed + 5)
            self._pwd_fwd.ChangeDutyCycle(speed * self._correction)
            self._pwd_rev.ChangeDutyCycle(0)

    def reverse( self, speed ):
        if self._initialized:
            speed = validate_max100(speed)
            self._pwd_rev.ChangeFrequency(speed + 5)
            self._pwd_rev.ChangeDutyCycle(speed * self._correction)
            self._pwd_fwd.ChangeDutyCycle(0)

    def stop( self ):
        if self._initialized:
            self._pwd_rev.ChangeDutyCycle(0)
            self._pwd_fwd.ChangeDutyCycle(0)


class Sensor(object):
    def __init__( self, pin ):
        self._pin = pin
        self._initialized = False

    def init( self ):
        if not self._initialized:
            GPIO.setup(self._pin, GPIO.IN)
            self._initialized = True
    
    def cleanup( self ):
        if self._initialized:
            self.remove_callbacks()
            GPIO.cleanup(self._pin)
            self._initialized = False
    
    @property
    def activated( self ):
        if self._initialized:
            if GPIO.input(self._pin) == 0:
                return True
            else:
                return False

    def _generate_callback( self, callback ):
        def _call_callback( pin ):
            state = self.activated
            callback(self._pin, state)
        return _call_callback

    def register_off_callback( self, callback ):
        if self._initialized:
            fce_to_call = self._generate_callback(callback)
            GPIO.add_event_detect(self._pin, GPIO.RISING, callback=fce_to_call, bouncetime=100)

    def register_on_callback( self, callback ):
        if self._initialized:
            fce_to_call = self._generate_callback(callback)
            GPIO.add_event_detect(self._pin, GPIO.FALLING, callback=fce_to_call, bouncetime=100)

    def register_both_callbacks( self, callback ):
        if self._initialized:
            fce_to_call = self._generate_callback(callback)
            GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=fce_to_call, bouncetime=100)

    def remove_callbacks( self ):
        if self._initialized:
            GPIO.remove_event_detect(self._pin)


class Switch(Sensor):
    def init( self ):
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._initialized = True

class WhiteLED(object):
    def __init__( self, pin ):
        self._pin = pin
        self._initialized = False

    def init( self ):
        if not self._initialized:
            GPIO.setup(self._pin, GPIO.OUT)
            self._pwm = GPIO.PWM(self._pin, 100)
            self._pwm.start(0)
            self._initialized = True
    
    def cleanup( self ):
        if self._initialized:
            self.off()
            GPIO.cleanup(self._pin)
            self._initialized = False
    
    def on( self ):
        self.set(100)

    def off( self ):
        self.set(0)

    def set( self, intensity ):
        if self._initialized:
            intensity = validate_max100(100 - intensity)
            self._pwm.ChangeDutyCycle(intensity)

    def brighten( self, delay = 0.1, step = 5 ):
        for dc in range(0, 101, step):
            self.set(dc)
            time.sleep(delay)

    def dim( self, delay = 0.1, step = 5 ):
        for dc in range(100, -1, step * -1):
            self.set(dc)
            time.sleep(delay)


class DistanceSensor(object):
    def __init__( self, pin ):
        self._pin = pin
        self.measure_running = threading.Event()

    def init( self ):
        pass

    def cleanup( self ):
        if self.measure_running.is_set:
            self.stop_distance_measure()
        GPIO.cleanup(self._pin)

    def _distance_measure( self, callback, delay = 1 ):
        if delay < 0.2: delay = 0.2
        while self.measure_running.is_set():
            distance = self.get_distance()
            callback(distance)
            time.sleep(delay)

    def start_distance_measure( self, callback, delay = 1 ):
        if not self.measure_running.is_set():
            if callable(callback):
                self._measure_thread = threading.Thread(target=self._distance_measure, args=(callback, delay))
                self.measure_running.set()
                self._measure_thread.start()
            else:
                raise AttributeError()

    def stop_distance_measure( self ):
        if self.measure_running.is_set():
            self.measure_running.clear()

    def get_distance( self ):
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
        return round(distance, 4)


class Servo(object):
    pass