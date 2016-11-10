from motors import Motors

class Motob():
    def __init__(self):
        self.motor = Motors()
        self.value = None # Most recent motor recommendation sent to the motob

    def update(self, motor_recom):
        self.value = motor_recom
        self.operationalize()

    def stop(self):
        self.motor.stop()

    def operationalize(self):
        if self.value[0] == "left":
            self.motor.stop()
            self.motor.turn_left(self.value[1])
            self.motor.forward(0.5)
        elif self.value[0] == "right":
            self.motor.stop()
            self.motor.turn_right(self.value[1])
            self.motor.forward(0.5)
        elif self.value[0] == "drive":
            self.motor.forward(self.value[1])
    
