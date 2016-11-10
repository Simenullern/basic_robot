from time import sleep
from reflectance_sensors import ReflectanceSensors
from camera import Camera
from motob import *
from zumo_button import ZumoButton
from arbitrator import Arbitrator
from sensob import *
from behavior import *
import datetime

class BBCON():

    def __init__(self,sensobs):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = sensobs
        self.motob = Motob()
        self.arbitrator = Arbitrator(self)

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    def run_one_timestep(self):
        a = datetime.datetime.now()
        for sensob in self.sensobs:
            sensob.update()
        b = datetime.datetime.now()
        print ("Time to fetch data was: ", b-a)

        c = datetime.datetime.now()
        for behavior in self.behaviors:
            behavior.update()
            if behavior.halt_request:
                self.motob.stop()
                return False
            if behavior.active_flag:
                self.activate_behavior(behavior)
            else:
                self.deactivate_behavior(behavior)
        winner = self.arbitrator.choose_action()
        self.motob.update(winner.motor_recommendation)
        print(winner.motor_recommendation)
        d = datetime.datetime.now()
        print("Time to calculate logic was: ", d - c)

        #sleep(0.1) #cnonsider there is already natural delay in motor turning actions
        e = datetime.datetime.now()
        for sensob in self.sensobs:
            sensob.reset()

        f = datetime.datetime.now()
        print("Time to reset sensors was: ", f - e)
        return True

def main():
    ZumoButton().wait_for_press()

    sensorUS = Ultrasonic()
    sensorIR =  IRProximitySensor()
    sensorReflect = ReflectanceSensors()

    sensob0 = US_Sensob(sensorUS)
    sensob1 = IRP_Sensob(sensorIR)
    sensob2 = Reflect_snap_Sensob(sensorReflect)

    bbcon = BBCON([sensob0, sensob1, sensob2])

    drive = Move_straight_ahead(bbcon)
    avoid_shit = Avoid_front_collision(bbcon,[sensob0, sensob1])
    snap_by_line = Snap_by_line(bbcon, [sensob2])

    bbcon.add_behavior(avoid_shit)
    bbcon.add_behavior(drive)
    bbcon.add_behavior(snap_by_line)

    keep_going = True
    while keep_going:
        keep_going = bbcon.run_one_timestep()

def test():
    sensor = ReflectanceSensors()

    for x in range(30):
        print(sensor.update())