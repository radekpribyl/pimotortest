from pi2golite import Pi2GoLiteConfig, Robot

class MalinaConfig(Pi2GoLiteConfig):
     def __init__(self):
         motor_left['revcorr'] = 7.6
         wheelsensors['avail'] = True
         servos['avail'] = True
         servos['param']['maxsteps'] = 238

r = Robot(MalinaConfig())
r.init()