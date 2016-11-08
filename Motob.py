from motors import Motors

class Motob():
    def __init__(self):
        self.motor = Motors()
        self.value = None # Most recent motor recommendation sent to the motob

    def update(self, motor_recom):
        self.value = motor_recom
        self.operationalize()

    def operationalize(self):
        pass

class Motob_avoid_front(Motob):

    def __init__(self):
        Motob.__init__()

    def operationalize(self):
        if self.value[0] == "left":
            self.motor.turn_left(self.value[1])
        elif self.value[1] == "right":
            self.motor.turn_right(self.value[1])

class Motob_move_straight_head(Motob):
    def __init__(self):
        Motob.__init__()

    def operationalize(self):
        self.motor.forward()



