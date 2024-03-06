import display
class Animations:
    """Animates card being hovered over (moves slightly up and stops).

        Parameters:
            image(string): A string(card image directory)
            rect(rect): A rect that's linked to the card
    """
    def card_hover(self, card):
        i = 0
        # Moves the card slightly up in 5 int increments to simulate a hover effect
        while i < 20:
            old_rect = [card[5].x, card[5].y]
            # Move card slightly up
            card[5].y += 1 # move card up slightly
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            # change positions of objects on screen
            # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
            display.Display.modify_objects_to_display(self, old_rect, new_rect)
            i += 1
        #ERROR! Fix card collision boxes,
        # also do this:  card animating = true  and replace the card in self.player_cards to the new one
        # check that if card is not being hovered over, then return to original position 
    def card_cant_select(self, card_rect):
        return 1
    def card_select_move(self, card_rect):
        return 1   