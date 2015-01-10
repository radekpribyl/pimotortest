import os
from robot.controls import Pi2GoRobot
basedir = os.path.abspath(os.path.dirname(__file__))

#Helper functions
def robotimport():
    robot = None
    try:
        robot  = __import__('pi2go')
    except:
        robot = __import__('pi2gomock')
    return robot

#Actual config classes
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'fdsafsfdsafdsafh;ljh'
    ROBOT = Pi2GoRobot()

class MalinaConfig(Config):
    pass
    #ROBOT = robotimport()

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    #ROBOT = __import__('pi2gomock')
    #ROBOT = robotimport()


    