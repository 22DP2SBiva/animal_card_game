import pygame
import display
# pylint doest accept dynamically generated code, must use disable no member
#pylint: disable=no-member
SPEED = 2
SELECT_POSITION_X = 200
SELECT_POSITION_Y = 400
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
        # Find and replace old_pos in objects we want to display with the new position
        # change positions of objects on screen
        # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        display.Display.modify_objects_to_display(self, old_rect, new_rect)
    def move_to_starting_pos(self, card):
        # Moves card back to the starting position
        # Checks if card current position X is the same as the starting position X
        old_rect = [card[5].x, card[5].y] # create a new rect that points to the old card rect
        new_rect = [card[5].x, card[5].y]
        if card[5].x != card[8][0]:
            card[5].x -= SPEED # move card up slightly
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            # change positions of objects on screen
            # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        if card[5].y != card[8][1]:
            card[5].y -= SPEED # move card up slightly
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            # change positions of objects on screen
            # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        display.Display.modify_objects_to_display(self, old_rect, new_rect)
    def card_cant_select(self, card):
        return 1
    def card_select(self, card):
        # Moves the card slightly up in 5 int increments to simulate a hover effect
        old_rect = [card[5].x, card[5].y] # create a new rect that points to the old card rect
        new_rect = [card[5].x, card[5].y]
        if card[5].x != SELECT_POSITION_X:
            card[5].x -= SPEED # move card up slightly
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            # change positions of objects on screen
            # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        if card[5].y != SELECT_POSITION_Y:
            card[5].y -= SPEED # move card up slightly
            new_rect = [card[5].x, card[5].y]
        # Find and replace old_pos in objects we want to display with the new position
        # change positions of objects on screen
        # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        display.Display.modify_objects_to_display(self, old_rect, new_rect)
    def card_select_move(self, card):
        return 1   