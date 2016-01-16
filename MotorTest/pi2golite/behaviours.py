"""
This modules defines behaviours for Pi2Go Lite robot

Author: Radek Pribyl
"""
from pi2golite._helpers import validate_max
import math
import time

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
        self._last_action = self.stop
        self._last_action_arguments = None

    def stop_left(self):
        self._left_motor.stop()

    def stop_right(self):
        self._right_motor.stop()

    def forward(self):
        self._go_forward(self._curr_speed, self._curr_speed)
        self._last_action = self.forward
        self._last_action_arguments = None

    def reverse(self):
        self._go_reverse(self._curr_speed, self._curr_speed)
        self._last_action = self.reverse
        self._last_action_arguments = None

    def spin_left(self):
        self._left_motor.reverse(self._curr_speed)
        self._right_motor.forward(self._curr_speed)
        self._last_action = self.spin_left
        self._last_action_arguments = None

    def spin_right(self):
        self._left_motor.forward(self._curr_speed)
        self._right_motor.reverse(self._curr_speed)
        self._last_action = self.spin_right
        self._last_action_arguments = None

    def turn_left(self, lf_pct=50):
        lf_speed = float(validate_max(lf_pct)) / 100 * self._curr_speed
        self._go_forward(lf_speed, self._curr_speed)
        self._last_action = self.turn_left
        self._last_action_arguments = {'lf_pct' : lf_pct}

    def turn_right(self, rg_pct=50):
        rg_speed = float(validate_max(rg_pct)) / 100 * self._curr_speed
        self._go_forward(self._curr_speed, rg_speed)
        self._last_action = self.turn_right
        self._last_action_arguments = {'rg_pct' : rg_pct}

    def turn_rev_left(self, lf_pct=50):
        lf_speed = float(validate_max(lf_pct)) / 100 * self._curr_speed
        self._go_reverse(lf_speed, self._curr_speed)
        self._last_action = self.turn_revleft
        self._last_action_arguments = {'lf_pct' : lf_pct}

    def turn_rev_right(self, rg_pct=50):
        rg_speed = float(validate_max(rg_pct)) / 100 * self._curr_speed
        self._go_reverse(self._curr_speed, rg_speed)
        self._last_action = self.turn_rev_right
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
    def __init__(self, steering, whl_counter_lf, whl_counter_rg, whl_sen_lf, whl_sen_rg):
        self._steering = steering
        self._whl_counter_lf = whl_counter_lf
        self._whl_counter_rg = whl_counter_rg
        self._whl_sen_lf = whl_sen_lf
        self._whl_sen_rg = whl_sen_rg
        self._lf_motor_running = False
        self._rg_motor_running = False

    def _wait_while_running(self):
        while self._lf_motor_running and self._rg_motor_running:
            time.sleep(0.01)
        self._steering.stop()

    def _stop_left(self):
        self._steering.stop_left()
        self._lf_motor_running = False

    def _stop_right(self):
        self._steering.stop_right()
        self._rg_motor_running = False

    def _run_both_motors(self, action, steps):
        if steps > 0:
            self._lf_motor_running = True
            self._rg_motor_running = True
            self._whl_counter_lf.start(steps, self._stop_left)
            self._whl_counter_rg.start(steps, self._stop_right)
            action()
            self._wait_while_running()

    def _run_left_motor(self, action, steps, *args):
        if steps > 0:
            self._lf_motor_running = True
            self._whl_counter_lf.start(steps, self._stop_left)
            action(*args)
            self._wait_while_running()

    def _run_right_motor(self, action, steps, *args):
        if steps > 0:
            self._rg_motor_running = True
            self._whl_counter_rg.start(steps, self._stop_right)
            action(*args)
            self._wait_while_running()

    def _run_and_count(self, action, lf_steps, rg_steps):
        #Init - prepare
        if lf_steps < 0:
            lf_steps = 0

        if rg_steps < 0:
            rg_steps = 0

        lf_count = 0
        rg_count = 0
        lf_lst_pos = self._whl_sen_lf.activated
        rg_lst_pos = self._whl_sen_rg.activated
        
        action()

        while lf_count < lf_steps or rg_count < rg_steps:
            time.sleep(0.002)
            lf_cur_pos = self._whl_sen_lf.activated
            if lf_cur_pos != lf_lst_pos:
                lf_count +=1
                lf_lst_pos = lf_cur_pos
                if lf_count >= lf_steps:
                    self._stop_left()

            rg_cur_pos = self._whl_sen_rg.activated
            if rg_cur_pos != rg_lst_pos:
                rg_count += 1
                rg_lst_pos = rg_cur_pos
                if rg_count >= rg_steps:
                    self._stop_right()
            

        self._steering.stop()

    def forward(self, steps):
        #self._run_both_motors(self._steering.forward, steps)
        self._run_and_count(self._steering.forward, steps, steps)

    def reverse(self, steps):
        #self._run_both_motors(self._steering.reverse, steps)
        self._run_and_count(self._steering.reverse, steps, steps)

    def spin_left(self, steps):
        #self._run_both_motors(self._steering.spin_left, steps)
        self._run_and_count(self._steering.spin_left, steps, steps)

    def spin_right(self, steps):
        #self._run_both_motors(self._steering.spin_right, steps)
        self._run_and_count(self._steering.spin_right, steps, steps)

    def turn_left(self, steps):
        #self._run_right_motor(self._steering.turn_left, steps, 0)
        action = lambda : self._steering.turn_left(0)
        self._run_and_count(action, 0, steps)

    def turn_right(self, steps):
        #self._run_left_motor(self._steering.turn_right, steps, 0)
        action = lambda : self._steering.turn_right(0)
        self._run_and_count(action, steps, 0)

    def turn_rev_left(self, steps):
        #self._run_right_motor(self._steering.turn_rev_left, steps, 0)
        action = lambda : self._steering.turn_rev_left(0)
        self._run_and_count(action, 0, steps)

    def turn_rev_right(self, steps):
        #self._run_left_motor(self._steering.turn_rev_right, steps, 0)
        action = lambda : self._steering.turn_rev_right(0)
        self._run_and_count(action, steps, 0)

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
        self._robot_width = robot_width
        self._step_dist = math.pi * whl_diameter / numsteps

    def _calc_steps_from_dist(self, dist):
        return round(dist / self._step_dist)

    def _calc_steps_from_angle(self, angle, spin=False):
        angle = validate_max(angle, 360)
        #For turning the robot width is radius, for spin diameter
        if spin:
            const = 1
        else:
            const = 2
        return angle * math.pi * const * self._robot_width / 360 / self._step_dist

    def forward(self, distance):
        if distance > 0:
            steps = self._calc_steps_from_dist(distance)
            self._step_steering.forward(steps)

    def reverse(self, distance):
        if distance > 0:
            steps = self._calc_steps_from_dist(distance)
            self._step_steering.reverse(steps)

    def spin_left(self, angle):
        steps = self._calc_steps_from_angle(angle, True)
        self._step_steering.spin_left(steps)

    def spin_right(self, angle):
        steps = self._calc_steps_from_angle(angle, True)
        self._step_steering.spin_right(steps)

    def turn_left(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_left(steps)

    def turn_right(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_right(steps)

    def turn_rev_left(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_rev_left(steps)

    def turn_rev_right(self, angle):
        steps = self._calc_steps_from_angle(angle)
        self._step_steering.turn_rev_right(steps)
