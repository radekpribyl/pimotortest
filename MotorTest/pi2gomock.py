from __future__ import print_function
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

def turnForwardLeft(speed):
    print("Zatoc dopredu doleva: " + str(speed))

def turnForwardRight(speed):
    print("Zatoc dopredu dopredu: " + str(speed))

def turnReverseLeft(speed):
    print("Zatoc dozadu doleva: " + str(speed))

def turnReverseRight(speed):
    print("Zatoc dozadu doprava: " + str(speed))