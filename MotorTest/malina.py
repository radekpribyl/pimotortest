from pi2golite import Pi2GoLiteConfig, Robot

class MalinaConfig(Pi2GoLiteConfig):
     def __init__(self):
         self.motor_right['fwdcorr'] = 4.5
         self.motor_left['revcorr'] = 0
         self.wheelsensors['avail'] = True
         self.servos['avail'] = True
         self.servos['param']['maxsteps'] = 238
         self.wheelsensors['measure_param']['whl_diameter'] = 6.55

r = Robot(MalinaConfig())
r.init()