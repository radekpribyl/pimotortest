import os
from pi2golite import Robot
basedir = os.path.abspath(os.path.dirname(__file__))

#Helper functions
def robotimport():
    robot = None
    try:
        robot = __import__('pi2go')
    except:
        robot = __import__('pi2gomock')
    return robot

#Actual config classes
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'fdsafsfdsafdsafh;ljh'
    ROBOT = Robot()

class MalinaConfig(Config):
    DEBUG = True
    TESTING = True
    #ROBOT = robotimport()
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    #ROBOT = __import__('pi2gomock')
    #ROBOT = robotimport()


    