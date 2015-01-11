from __future__ import print_function
from random import randrange

OUT = 0
IN = 1
BOARD = 0
RISING = 0
BOTH = 0
PUD_UP = 0

def setup(pin, type, pull_up_down=PUD_UP):
    pass

def setmode(mode):
    pass

def input(pin):
    return bool(randrange(0, 2))

def output(pin, value):
    pass

def cleanup(pin=0):
    pass

def add_event_detect(pin, type, callback=None, bouncetime=100):
    pass

def remove_event_detect(pin):
    pass

class PWM:
    def __init__(self, pin, freq):
        self.pin = pin
        self.freq = freq
        self.dc = 0
    def ChangeFrequency(self, freq):
        self.freq = freq
        print("Changing frequency on pin: %s to: %s" % (self.pin, self.freq))
    def ChangeDutyCycle(self, dc):
        self.dc = dc
        print("Changing dc on pin: %s to: %s" % (self.pin, self.dc))
    def start(self, dc):
        self.dc = dc