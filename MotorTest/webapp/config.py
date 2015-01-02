import os
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

class MalinaConfig(Config):
    ROBOT = robotimport()

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    ROBOT = __import__('pi2gomock')
    #ROBOT = robotimport()


    