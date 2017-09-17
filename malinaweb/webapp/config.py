from pi2golite import Robot

#Actual config classes
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'fdsafsfdsafdsafh;ljh'
    ROBOT = Robot()


class MalinaConfig(Config):
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    