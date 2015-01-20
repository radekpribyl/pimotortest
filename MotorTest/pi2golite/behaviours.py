"""
This modules defines behaviours for Pi2Go Lite robot

Author: Radek Pribyl
"""
from pi2golite._helpers import validate_max
import math

class Steering(object):
    """
    Class defining basic movement actions of Pi2Go lite in
    various directions. It also takes care about robot's speed

    :param  lf_motor: instance of Motor class defining left motor
            rg_motor: instance of Motor class defining right motor
            init_speed: initial speed of the robot. Speed can be in
            range of 0 to 100
    """
    def __init__(self, lf_motor, rg_motor, init_speed=20):
        self._left_motor = lf_motor
        self._right_motor = rg_motor
        self._curr_speed = init_speed
        self._last_action = Steering.stop
        self._last_action_arguments = None

    def cleanup(self):
        self._left_motor.cleanup()
        self._right_motor.cleanup()

    @property
    def current_speed(self):
        return self._curr_speed

    def _exec_last_action(self):
        if self._last_action_arguments is None:
            self._last_action(self)
        else:
            self._last_action(self, **self._last_action_arguments)

    def _go_forward(self, lf_speed, rg_speed):
        self._left_motor.forward(lf_speed)
        self._right_motor.forward(rg_speed)

    def _go_reverse(self, lf_speed, rg_speed):
        self._left_motor.reverse(lf_speed)
        self._right_motor.reverse(rg_speed)

    def stop(self):
        self._left_motor.stop()
        self._right_motor.stop()
        self._last_action = Steering.stop
        self._last_action_arguments = None

    def stop_left(self):
        self._left_motor.stop()

    def stop_right(self):
        self._right_motor.stop()

    def forward(self):
        self._go_forward(self._curr_speed, self._curr_speed)
        self._last_action = Steering.forward
        self._last_action_arguments = None

    def reverse(self):
        self._go_reverse(self._curr_speed, self._curr_speed)
        self._last_action = Steering.reverse
        self._last_action_arguments = None

    def spin_left(self):
        self._left_motor.reverse(self._curr_speed)
        self._right_motor.forward(self._curr_speed)
        self._last_action = Steering.spin_left
        self._last_action_arguments = None

    def spin_right(self):
        self._left_motor.forward(self._curr_speed)
        self._right_motor.reverse(self._curr_speed)
        self._last_action = Steering.spin_right
        self._last_action_arguments = None

    def turn_forward_left(self, lf_pct=50):
        lf_speed = float(validate_max(lf_pct)) / 100 * self._curr_speed
        self._go_forward(lf_speed, self._curr_speed)
        self._last_action = Steering.turn_forward_left
        self._last_action_arguments = {'lf_pct' : lf_pct}

    def turn_forward_right(self, rg_pct=50):
        rg_speed = float(validate_max(rg_pct)) / 100 * self._curr_speed
        self._go_forward(self._curr_speed, rg_speed)
        self._last_action = Steering.turn_forward_right
        self._last_action_arguments = {'rg_pct' : rg_pct}

    def turn_reverse_left(self, lf_pct=50):
        lf_speed = float(validate_max(lf_pct)) / 100 * self._curr_speed
        self._go_reverse(lf_speed, self._curr_speed)
        self._last_action = Steering.turn_reverse_left
        self._last_action_arguments = {'lf_pct' : lf_pct}

    def turn_reverse_right(self, rg_pct=50):
        rg_speed = float(validate_max(rg_pct)) / 100 * self._curr_speed
        self._go_reverse(self._curr_speed, rg_speed)
        self._last_action = Steering.turn_reverse_right
        self._last_action_arguments = {'rg_pct' : rg_pct}

    def set_speed(self, speed):
        speed = validate_max(speed)
        self._curr_speed = speed
        self._exec_last_action()
        return self._curr_speed

    def increase_speed(self, increment=10):
        speed = self._curr_speed + increment
        return self.set_speed(speed)

    def decrease_speed(self, decrement=10):
        speed = self._curr_speed - decrement
        return self.set_speed(speed)

class StepSteering(object):
    """
    Class defining movement actions of Pi2Go lite using wheel counters.
    The class uses instance of Steering for performing the actual
    movements and WheelCounter instances to stop the motors after
    defined number of steps

    :param  steering: instance of Steering class for movement delegation
            whl_counter_lf: instance of WheelCounter for left motor
            whl_counter_rg: instance of WheelCounter for right motor
    """
    def __init__(self, steering, whl_counter_lf, whl_counter_rg):
        self._steering = steering
        self._whl_counter_lf = whl_counter_lf
        self._whl_counter_rg = whl_counter_rg

    def forward(self, steps):
        if steps > 0:
            self._whl_counter_lf.start(steps)
            self._whl_counter_rg.start(steps)
            self._steering.forward()

    def reverse(self, steps):
        if steps > 0:
            self._whl_counter_lf.start(steps)
            self._whl_counter_rg.start(steps)
            self._steering.reverse()

    def spin_left(self, steps):
        if steps > 0:
            self._whl_counter_lf.start(steps)
            self._whl_counter_rg.start(steps)
            self._steering.spin_left()

    def spin_right(self, steps):
        if steps > 0:
            self._whl_counter_lf.start(steps)
            self._whl_counter_rg.start(steps)
            self._steering.spin_right()

    def turn_forward_left(self, steps):
        if steps > 0:
            self._whl_counter_rg.start(steps)
            self._steering.turn_forward_left(0)

    def turn_forward_right(self, steps):
        if steps > 0:
            self._whl_counter_lf.start(steps)
            self._steering.turn_forward_right(0)

    def turn_reverse_left(self, steps):
        if steps > 0:
            self._whl_counter_rg.start(steps)
            self._steering.turn_reverse_left(0)

    def turn_reverse_right(self, steps):
        if steps > 0:
            self._whl_counter_lf.start(steps)
            self._steering.turn_reverse_right(0)

class MeasureSteering(object):
    """
    Class defining movement actions of Pi2Go lite using distance unit
    (if class initiated with whl_diameter and robot_width e.g. in centimeters
    then the distance should be in centimeters too). Angles are to be provided
    in degrees (in range of 0 to 360)
    The class recalculates the distance units and ange degrees to steps and
    delegates to instance of StepSteering to perform the movement

    :param  step_steering: instance of StepSteering class for movement delegation
            whl_diameter: diameter of the wheel - default wheels should be 65 mm / 6.5 cm
            robot_width: width of the robot - used in angles calculation
            numsteps: number of steps on WheelCounter. Provided wheelcounters have 16 steps

    Please note that the precision of the movement is determined by the number of steps on
    wheelcounters so it cannot be 100% precise.
    """
    def __init__(self, step_steering, whl_diameter, robot_width, numsteps):
        self._step_steering = step_steering
        self._step_dist = math.pi * whl_diameter / numsteps
        self._angle_dist = math.pi * 2 * robot_width / 360

    def _calc_steps_from_dist(self, dist):
        return round(dist / self._step_dist)

    def _calc_steps_from_angle(self, angle):
        angle = validate_max(angle, 360)
        return angle * self._angle_dist / self._step_dist

    def forward(self, distance):
        if distance > 0:
            steps = self._calc_steps_from_dist(distance)
            self._step_steering.forward(steps)

    def reverse(self, distance):
        if distance > 0:
            steps = self._calc_steps_from_dist(distance)
            self._step_steering.reverse(steps)

    def turn_forward_left(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_forward_left(steps)

    def turn_forward_right(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_forward_right(steps)

    def turn_reverse_left(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_reverse_left(steps)

    def turn_reverse_right(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_reverse_right(steps)
