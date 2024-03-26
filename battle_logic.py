class Battle_Logic:
    # Determine battle outcome
    #                  attacking_card, defending_card
    def determine_outcome(self, card1, card2):
        # Check which cards' tier is higher
        if card1[1] > card2[1]:
            winner = card1
        elif card1[1] == card2[1]:
            winner = None
        else:
            winner = card2
        return winner