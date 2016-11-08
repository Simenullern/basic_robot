class Arbitrator():

    def __int__(self, bbcon):
        self.bccon = bbcon

    def choose_action(self):
        # Største vekt vinner
        winner = None

        for behavior in self.bccon.active_behaviors:
            if not winner:
                winner = behavior
            elif behavior.weight > winner.weight:
                winner = behavior

        if not winner:
            print ("Noe gikk alvorlig galt. Ingen aktive behaviors. Er det ikke en default active behavior?")

        return winner