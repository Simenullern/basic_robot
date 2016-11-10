import random

class Behavior():

    def __init__(self, bbcon, sensobs, priority):
        self.bbcon = bbcon #pointer to the controller
        self.sensobs = sensobs # type list containing sensor object
        self.motor_recommendation = None # tuple
        self.priority = priority # a static value indicating importance of this behavior
        self.active_flag = False # If this behavior is active or not
        self.halt_request = False # some behaviors can request the robot to completely halt activity (and thus end the run).
        self.match_degree = None  # A real number in the range [0, 1], higher == more weight
        self.weight = None # the product of mathch_degree and priority

    def update(self):
        self.active_flag = self.consider_activation()

        if self.active_flag:
            self.sense_and_act()
            self.weight = self.priority * self.match_degree

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def sense_and_act(self):
        pass

class Move_straight_ahead(Behavior):

    def __init__(self, bbcon, sensobs = [], priority = 1, motor_recom = ("drive", 0.5)):
        Behavior.__init__(self, bbcon, sensobs, priority)
        self.motor_recommendation = motor_recom
        self.active_flag = True
        self.match_degree = 0.01 # super small default behavior

    def consider_activation(self):
        return True

class Avoid_front_collision(Behavior):

    #Sensobs = [front, sider]
    def __init__(self, bbcon, sensobs, priority = 8): # assume priority in range [1,10]
        Behavior.__init__(self, bbcon, sensobs, priority)

    def consider_activation(self):
        return self.sensobs[0].get_value() < 40 and self.sensobs[0].get_value() > 1 or self.sensobs[1].get_value()[0] or self.sensobs[1].get_value()[1] # aktiv når mindre enn en 40cm

    def consider_deactivation(self):
        return not self.consider_activation()

    def sense_and_act(self):
        for sensob in self.sensobs:
            sensob.update()

        if self.sensobs[1].get_value()[1]:
            print("Objekt detektert paa hoyre side!")
            self.match_degree = 0.99
            self.motor_recommendation = ("left", 90)

        elif self.sensobs[1].get_value()[0]:
            print("Objekt detektert paa venstre side!")
            self.match_degree = 0.99
            self.motor_recommendation = ("right", 90)

        else:
            print("Objekt detektert foran!")
            self.match_degree = 1 - (self.sensobs[0].get_value()/40)
            self.motor_recommendation = (random.choice(["left", "right"]),random.randint(80, 100))

class Snap_by_line(Behavior):

    def __init__(self, bbcon, sensobs, priority = 6):
        Behavior.__init__(self, bbcon, sensobs, priority)
        self.sensob = self.sensobs[0]
        self.cam = self.sensobs[1]
        self.count = 1

    def consider_activation(self):
        return self.sensob.get_value()

    def consider_deactivation(self):
        return not self.consider_deactivation()

    def sense_and_act(self):

        self.cam.get_value().dump_image("line_number"+str(self.count)+".jpeg")
        print("Bilde nummer "+ str(self.count)+ " tatt!")
        self.count += 1

        self.match_degree = 0.5
        self.motor_recommendation = ("right", 540)

        if self.count > 3:
            self.halt_request = True
            print ("Task complete. Robot going to sleep.")
            self.motor_recommendation = ("drive", 0)