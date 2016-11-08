
class Behavior():

    def __init__(self, bbcon, sensobs, priority):
        self.bbcon = bbcon #pointer to the controller
        self.sensobs = sensobs # type list containing sensor object
        self.motor_recommendations = [] # list of recommendations, one per motob
        self.priority = priority # a static value indicating importance of this behavior
        self.active_flag = False # If this behavior is active or not
        self.halt_request = None # some behaviors can request the robot to completely halt activity (and thus end the run).
        self.match_degree = None  # A real number in the range [0, 1], higher == more weight
        self.weight = None # the product of mathch_degree and priority

    def update(self):
        self.active_flag = self.consider_activation()

        if self.active_flag:
            match_degree = self.sense_and_act()
            self.weight = self.priority * match_degree

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def sense_and_act(self):
        pass

class move_straight_ahead(Behavior):

    def __init__(self, bbcon, sensobs = [], priority = 1, motor_recoms = []):
        Behavior.__init__(self, bbcon, sensobs, priority)
        self.motor_recommendations = motor_recoms
        self.active_flag = True
        self.match_degree = 0.01 # super small default behavior


class avoid_front_collision(Behavior):

    def __init__(self, bbcon, sensobs, priority = 8, motor_recoms = [("left", 90)]): # assume priority in range [1,10]
        Behavior.__init__(self, bbcon, sensobs, priority)
        self.motor_recommendations = motor_recoms

    """ anta at ultrasonic er på index 0 og at det kun er dette vi vurderer for denne klassen """

    def consider_activation(self):
        return self.sensobs[0].get_value() < 100 # aktiv når mindr enn en meter

    def consider_deactivation(self):
        return not self.consider_activation()

    def sense_and_act(self):
        for sensob in self.sensobs:
            sensob.update()

        self.match_degree = 1 - (self.sensobs[0].get_value()/100)
        #=> degree 0 if distance is 100 cm, degree 0.9 if distaince is 10 cm

