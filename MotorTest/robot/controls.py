# Python Module to control HW aspects of Pi2Go robot
# Provides access to basic functions of the Pi2Go robot
# No logic included in this module

#Import all modules/libraries
import time
try:
    import RPi.GPIO as GPIO
except ImportError:
    import dummyGPIO as GPIO

#Helper functions
def _check_pwm_value( intensity ):
    if intensity > 99:
        intensity = 100
    elif intensity < 1:
        intensity = 0
    return intensity

def _clean_speed_freq( lf_speed, rg_speed ):
    lf_speed = _check_pwm_value(lf_speed)
    rg_speed = _check_pwm_value(rg_speed)    

    if rg_speed > lf_speed:
        freq = lf_speed + 5
    else:
        freq = rg_speed + 5
    return (lf_speed, rg_speed, freq)

#Classes
class Motor(object):
    def __init__( self, pin_lf1, pin_lf2, pin_rg1, pin_rg2, corr_lf = 0, corr_rg = 0, init_speed = 20 ):
        self._pin_lf1 = pin_lf1
        self._pin_lf2 = pin_lf2
        self._pin_rg1 = pin_rg1
        self._pin_rg2 = pin_rg2
        self._corr_lf = 1 - (corr_lf / 100)
        self._corr_rg = 1 - (corr_rg / 100)
        self._curr_speed = init_speed
        self._initialized = False
        
    def init( self ):
        if not self._initialized:
            GPIO.setup(self._pin_lf1, GPIO.OUT)
            GPIO.setup(self._pin_lf2, GPIO.OUT)
            GPIO.setup(self._pin_rg1, GPIO.OUT)
            GPIO.setup(self._pin_rg2, GPIO.OUT)
            self._pwm_lff = GPIO.PWM(self._pin_lf1, self._curr_speed)
            self._pwm_lfr = GPIO.PWM(self._pin_lf2, self._curr_speed)
            self._pwm_rgf = GPIO.PWM(self._pin_rg1, self._curr_speed)
            self._pwm_rgr = GPIO.PWM(self._pin_rg2, self._curr_speed)
            self._pwm_lff.start(0)
            self._pwm_lfr.start(0)
            self._pwm_rgf.start(0)
            self._pwm_rgr.start(0)
            self._last_action = Motor.stop
            self._last_action_arguments = None
            self._initialized = True

    def cleanup( self ):
        if self._initialized:
            del self._pwm_lff
            del self._pwm_lfr
            del self._pwm_rgf
            del self._pwm_lfr
            del _last_action
            self._initialized = False

    def _exec_last_action( self ):
        if self._initialized:
            if self._last_action_arguments is None:
                self._last_action(self)
            else:
                self._last_action(self, **self._last_action_arguments)

    def _go_forward( self, lf_speed, rg_speed ):
        if self._initialized:
            lf_speed, rg_speed, freq = _clean_speed_freq(lf_speed, rg_speed)

            self._pwm_lff.ChangeFrequency(freq)
            self._pwm_rgf.ChangeFrequency(freq)
            self._pwm_lff.ChangeDutyCycle(lf_speed * self._corr_lf)
            self._pwm_lfr.ChangeDutyCycle(0)
            self._pwm_rgf.ChangeDutyCycle(rg_speed * self._corr_rg)
            self._pwm_rgr.ChangeDutyCycle(0)

    def _go_reverse( self, lf_speed, rg_speed ):
        if self._initialized:
            lf_speed, rg_speed, freq = _clean_speed_freq(lf_speed, rg_speed)

            self._pwm_lfr.ChangeFrequency(freq)
            self._pwm_rgr.ChangeFrequency(freq)
            self._pwm_lff.ChangeDutyCycle(0)
            self._pwm_lfr.ChangeDutyCycle(lf_speed * self._corr_lf)
            self._pwm_rgf.ChangeDutyCycle(0)
            self._pwm_rgr.ChangeDutyCycle(rg_speed * self._corr_rg)

    def stop( self ):
        if self._initialized:
            self._go_forward(0,0)
            self._last_action = Motor.stop
            self._last_action_arguments = None

    def stop_left( self ):
        if self._initialized:
            self._pwm_lff.ChangeDutyCycle(0)
            self._pwm_lfr.ChangeDutyCycle(0)

    def stop_right( self ):
        if self._initialized:
            self._pwm_rgf.ChangeDutyCycle(0)
            self._pwm_rgr.ChangeDutyCycle(0)

    def forward( self ):
        if self._initialized:
            self._go_forward(self._curr_speed, self._curr_speed)
            self._last_action = Motor.forward
            self._last_action_arguments = None

    def reverse( self ):
        if self._initialized:
            self._go_reverse(self._curr_speed, self._curr_speed)
            self._last_action = Motor.reverse
            self._last_action_arguments = None

    def spin_left( self ):
        if self._initialized:
            self._pwm_lfr.ChangeFrequency(self._curr_speed + 5)
            self._pwm_rgf.ChangeFrequency(self._curr_speed + 5)
            self._pwm_lff.ChangeDutyCycle(0)
            self._pwm_lfr.ChangeDutyCycle(self._curr_speed * self._corr_lf)
            self._pwm_rgf.ChangeDutyCycle(self._curr_speed * self._corr_rg)
            self._pwm_rgr.ChangeDutyCycle(0)
            self._last_action = Motor.spin_left
            self._last_action_arguments = None

    def spin_right( self ):
        if self._initialized:
            self._pwm_lff.ChangeFrequency(self._curr_speed + 5)
            self._pwm_rgr.ChangeFrequency(self._curr_speed + 5)
            self._pwm_lff.ChangeDutyCycle(self._curr_speed * self._corr_lf)
            self._pwm_lfr.ChangeDutyCycle(0)
            self._pwm_rgf.ChangeDutyCycle(0)
            self._pwm_rgr.ChangeDutyCycle(self._curr_speed * self._corr_rg)
            self._last_action = Motor.spin_right
            self._last_action_arguments = None

    def turn_forward_left( self, ratio = 2 ):
        if self._initialized:
            self._go_forward(self._curr_speed / ratio, self._curr_speed)
            self._last_action = Motor.turn_forward_left
            self._last_action_arguments = {'ratio' : ratio}

    def turn_forward_right( self, ratio = 2 ):
        if self._initialized:
            self._go_forward(self._curr_speed, self._curr_speed / ratio)
            self._last_action = Motor.turn_forward_right
            self._last_action_arguments = {'ratio' : ratio}

    def turn_reverse_left( self, ratio = 2 ):
         if self._initialized:
            self._go_reverse(self._curr_speed / ratio, self._curr_speed)
            self._last_action = Motor.turn_reverse_left
            self._last_action_arguments = {'ratio' : ratio}

    def turn_reverse_right( self, ratio = 2 ):
         if self._initialized:
            self._go_reverse(self._curr_speed, self._curr_speed / ratio)
            self._last_action = Motor.turn_reverse_right
            self._last_action_arguments = {'ratio' : ratio}

    def increase_speed( self, increment = 10 ):
        if self._initialized:
            self._curr_speed += increment
            if self._curr_speed > 99:
                self._curr_speed = 100
            self._exec_last_action()

    def decrease_speed( self, decrement = 10 ):
        if self._initialized:
            self._curr_speed -= decrement
            if self._curr_speed < 1:
                self._curr_speed = 0
            self._exec_last_action()

class IrSensor(object):
    def __init__( self, pin ):
        self._pin = pin
        self._initialized = False

    def init( self ):
        GPIO.setup(self._pin, GPIO.IN)

    def triggered( self ):
        if GPIO.input(self._pin) == 0:
            return True
        else:
            return False

    def register_raising_callback( self, callback ):
        GPIO.add_event_detect(self._pin, GPIO.RISING, callback=callback, bouncetime=200)

    def register_failing_callback( self, callback ):
        GPIO.add_event_detect(self._pin, GPIO.FALLING, callback=callback, bouncetime=200)

    def remove_callbacks( self ):
        GPIO.remove_event_detect(self._pin)

    def cleanup( self ):
        if self._initialized:
            self.remove_callbacks()
            self._initialized = False

class WhiteLED(object):
    def __init__( self, pin ):
        self._pin = pin
        self._initialized = False

    def init( self ):
        GPIO.setup(self._pin, GPIO.OUT)
        self._pwm = GPIO.PWM(self._pin, 100)
        self._pwm.start(0)
        self._initialized = True

    def on( self ):
        self.set(0)

    def off( self ):
        self.set(100)

    def set( self, intensity ):
        if self._initialized:
            intensity = _check_pwm_value(100 - intensity)
            self._pwm.ChangeDutyCycle(intensity)

    def brighten( self, delay = 0.1, step = 5 ):
        for dc in range(0, 101, step):
            self.set(dc)
            time.sleep(delay)

    def dim( self, delay = 0.1, step = 5 ):
        for dc in range(100, -1, step * -1):
            self.set(dc)
            time.sleep(delay)

    def cleanup( self ):
        if self._initialized:
            self.off()
            self._initialized = False

class DistanceSensor(object):
    pass

class Switch(object):
    pass

class Servo(object):
    pass

class Pi2GoRobot(object):
    def __init__( self ):
        self._components = []
        #Both motor setup
        self.motor = Motor(26,24,19,21, 7.3)
        self._components.append(self.motor)

        #While LEDs setup
        self.front_LED = WhiteLED(15)
        self.rear_LED = WhiteLED(16)
        self._components.append(self.front_LED)
        self._components.append(self.rear_LED)

        #IR sensors
        self.obstacle_left = IrSensor(7)
        self.obstacle_right = IrSensor(11)
        self.linesensor_left = IrSensor(12)
        self.linesensor_right = IrSensor(13)
        self._components.append(self.obstacle_left)
        self._components.append(self.obstacle_right)
        self._components.append(self.linesensor_left)
        self._components.append(self.linesensor_right)

        #Aliases for wheel sensors as they have to be switched
        #Pins are the same as for line sensors
        self.wheelsensor_left = self.linesensor_left
        self.wheelsensor_right = self.linesensor_right

    def robot_init( self ):
        GPIO.setmode(GPIO.BOARD)
        for component in self._components:
            component.init()

    def robot_cleanup( self ):
        for component in self._components:
            component.cleanup()
        GPIO.cleanup()