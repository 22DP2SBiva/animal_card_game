import pygame
import display
# pylint doest accept dynamically generated code, must use disable no member
#pylint: disable=no-member
SPEED = 3
class Animations:
    """Animates card being hovered over (moves slightly up and stops).

        Parameters:
            image(string): A string(card image directory)
            rect(rect): A rect that's linked to the card
    """
    def card_hover(self, card):
        # Moves the card slightly up in 5 int increments to simulate a hover effect
        old_rect = [card[5].x, card[5].y] # create a new rect that points to the old card rect
        # Move card slightly up
        card[5].y += SPEED # move card up slightly]
        new_rect = [card[5].x, card[5].y]
        print(old_rect)
        print(new_rect)
        # Find and replace old_pos in objects we want to display with the new position
        # change positions of objects on screen
        # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        display.Display.modify_objects_to_display(self, old_rect, new_rect)
    def move_to_starting_pos(self, card):
        print("entered method")
        # Moves card back to the starting position
        # Checks if card current position X is the same as the starting position X
        old_rect = [card[5].x, card[5].y] # create a new rect that points to the old card rect
        if card[5].x != card[8][0]:
            # ! CHANGE THIS SO THAT IT CHANGES X AND Y APPROPRIATELY (+ or -)
            card[5].x -= SPEED # move card up slightly
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            # change positions of objects on screen
            # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
            display.Display.modify_objects_to_display(self, old_rect, new_rect)
        if card[5].y != card[8][1]:
            card[5].y -= SPEED # move card up slightly
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            # change positions of objects on screen
            # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
            display.Display.modify_objects_to_display(self, old_rect, new_rect)
    def card_cant_select(self):
        return 1
    def card_select_move(self):
        return 1   