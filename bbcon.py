from time import sleep
import random
import imager2 as IMR
from reflectance_sensors import ReflectanceSensors
from camera import Camera
from motors import Motors
from motob import *
from ultrasonic import Ultrasonic
from irproximity_sensor import  IRProximitySensor
from zumo_button import ZumoButton
from arbitrator import Arbitrator
from sensob import *
import time
from behavior import *

class BBCON():

    def __init__(self,motob,sensobs):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = sensobs
        self.motob = motob
        self.arbitrator = Arbitrator(self)




    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        if(behavior in self.active_behaviors):
            self.active_behaviors.remove(behavior)


    def run_one_timestep(self):
        for sensob in self.sensobs:
            sensob.update()
        for behavior in self.behaviors:
            behavior.update()
            if behavior.active_flag:
                self.activate_behavior(behavior)
            else:
                self.deactivate_behavior(behavior)
        winner = self.arbitrator.choose_action()
        self.motob.update(winner.motor_recommendation)
        #time.sleep(0.1)
        for sensob in self.sensobs:
            sensob.reset()


def main():
    ZumoButton().wait_for_press()

    motob = Motob()

    sensorUS = Ultrasonic()
    sensorIR =  IRProximitySensor()
    sensorReflect = ReflectanceSensors()
    sensorCam = Camera()

    sensob0 = US_Sensob(sensorUS)
    sensob1 = IRP_Sensob(sensorIR)
    sensob2 = Reflect_Sensob(sensorReflect)
    sensob3 = Camera_Sensob(sensorCam)

    bbcon = BBCON(motob,[sensob0, sensob1, sensob2, sensob3])

    drive = Move_straight_ahead(bbcon)
    avoid_shit = Avoid_front_collision(bbcon,[sensob0, sensob1])
    snap_by_line = Snap_by_line(bbcon, [sensob2, sensob3])

    bbcon.add_behavior(avoid_shit)
    bbcon.add_behavior(drive)
    #bbcon.add_behavior(snap_by_line)


    for x in range(15):
        bbcon.run_one_timestep()
    Motors().stop()

def test():
    sensor = ReflectanceSensors()

    for x in range(30):
        print(sensor.update())

