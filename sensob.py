from ultrasonic import Ultrasonic
from irproximity_sensor import IRProximitySensor
from camera import Camera
import imager2 as IMR

# 1. reflectens (returnerer liste av 6 tall mellom 0 og 1)
# 2. distanse-måler (returnerer avstanden)
# 3. IR-målere (returnere liste true/false)
# 4. Kamera (returner image-objekt)

class Sensob():

    def __init__(self, sensor):
        self.sensor  = sensor # liste
        self.behaviors = []
        self.value = None

    def update(self):
        pass


    def get_value(self):
        return self.value


    def reset(self):
        self.sensor.reset()

class US_Sensob(Sensob):

    def __init__(self,sensor):
        Sensob.__init__(self,sensor)


    def update(self):
        self.sensor.update()
        self.value = self.sensor.get_value()
        print(self.value)


# IRP_Sensob.value er en tuppel på form (boolean,boolean) indeks1 er høyre og indeks0 er venstre
class IRP_Sensob(US_Sensob):

    def __init__(self, sensor):
        US_Sensob.__init__(self, sensor)

    def update(self):
        self.sensor.update()
        self.value = self.sensor.get_value()


class Reflect_snap_Sensob(Sensob):

    def __init__(self, sensor):
        Sensob.__init__(self, sensor)
        self.cam = Camera()

    def update(self):
        # only update sensors underneath!
        self.sensor.update()
        self.value = False
        for value in self.sensor.get_value():
            if value < 0.1:
                self.value = True
                break
        #self.value = sum(self.sensor.get_value()) < 1
        #print(self.sensor.get_value())

    def snap(self):
        return IMR.Imager(image=self.cam.get_value())
