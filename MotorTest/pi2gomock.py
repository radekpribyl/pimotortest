from __future__ import print_function
from random import randint
#My variables
isRobotInitiated = False
currentSpeed = 30

def init():
    pass

def cleanup():
    pass

def forward(speed):
    print("Vpred: " + str(speed))

def reverse(speed):
    print("Vzad: " + str(speed))

def stop(*args):
    print("Stop")

def spinLeft(speed):
    print("Rotuj doleva: " + str(speed))

def spinRight(speed):
    print("Rotuj doprava: " + str(speed))

def turnForward(leftSpeed, rightSpeed):
    print("Zatoc dopredu, leva rychlost: " + str(leftSpeed) + " prava: " + str(rightSpeed))

def turnreverse(leftSpeed, rightSpeed):
    print("Zatoc dozadu, leva rychlost: " + str(leftSpeed) + " prava: " + str(rightSpeed))

def turn_forward_left(speed):
    print("Zatoc dopredu doleva: " + str(speed))

def turn_forward_right(speed):
    print("Zatoc dopredu dopredu: " + str(speed))

def turn_reverse_left(speed):
    print("Zatoc dozadu doleva: " + str(speed))

def turn_reverse_right(speed):
    print("Zatoc dozadu doprava: " + str(speed))

def getDistance():
    return randint(0, 100)