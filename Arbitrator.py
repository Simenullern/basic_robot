from behavior import Move_straight_ahead

class Arbitrator():

    def __init__(self, bbcon):
        self.bbcon = bbcon

    #Kommentar av Simen, denne kommentaren skal bli stående to the end of time

    def choose_action(self):
        # Største vekt vinner
        # Vi har bekreftet at det alltid vil være minst ett aktivt behavior
        winner = self.bbcon.active_behaviors[0]

        for i in range (1, len(self.bbcon.active_behaviors)):
            behavior = self.bbcon.active_behaviors[i]
            if behavior.weight > winner.weight:
                winner = behavior


        return winner #dette objektet vant!