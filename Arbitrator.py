from behavior import Move_straight_ahead

class Arbitrator():

    def __init__(self, bbcon):
        self.bbcon = bbcon

    def choose_action(self):
        # Største vekt vinner
        winner = None

        for behavior in self.bbcon.active_behaviors:
            if not winner:
                winner = behavior
            elif behavior.weight > winner.weight:
                winner = behavior

        if not winner:
            #winner = Move_straight_ahead(self.bbcon)
            print ("NO ACTIVE BEHAVIORS!")

        return winner