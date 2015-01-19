from pi2golite import Pi2GoLiteConfig, Robot

class MalinaConfig(Pi2GoLiteConfig):
     def __init__(self):
         self.motor_left['revcorr'] = 7.6
         self.wheelsensors['avail'] = True
         self.servos['avail'] = True
         self.servos['param']['maxsteps'] = 238

r = Robot(MalinaConfig())
r.init()