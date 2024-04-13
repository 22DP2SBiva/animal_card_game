import pygame
import math
import display
# pylint doest accept dynamically generated code, must use disable no member
#pylint: disable=no-member
SPEED = 2
FAST_SPEED = 30
SELECT_POSITION_X = 900
SELECT_POSITION_Y = 420
class Animations:
    """Animates card being hovered over (moves slightly up and stops).

        Parameters:
            image(string): A string(card image directory)
            rect(rect): A rect that's linked to the card
    """
    def card_hover(self, card):
        i = 0
        start_rect = [card[5].x, card[5].y]
        while i < SPEED: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
            print("Frame" + str(i))
            # Moves the card slightly up in 5 int increments to simulate a hover effect
            old_rect = [card[5].x, card[5].y] # create a new rect that points to the old card rect
            # Move card slightly up
            card[5].y += 1 # move card up slightly]
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            # change positions of objects on screen
            # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
            i += 1
        displayy = display.Display
        displayy.modify_objects_to_display(self, start_rect, new_rect, False)
    def move_to_starting_pos(self, card, no_cards_have_attacked_yet, new_position):
        i = 0
        start_rect = [card[5].x, card[5].y]
        while i < SPEED: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
            # Moves card back to the starting position
            # Checks if card current position X is the same as the starting position X
            new_rect = [card[5].x, card[5].y]
            # Checks x and y positions of card and desired position, then moves it accordingly
            if no_cards_have_attacked_yet:
                if card[5].x != card[8][0]:

                    if card[5].x > card[8][0]:
                        card[5].x -= 1 # move card left slightly
                        new_rect = [card[5].x, card[5].y]
                    if card[5].x < card[8][0]:
                        card[5].x += 1 # move card right slightly
                        new_rect = [card[5].x, card[5].y]

                if card[5].y != card[8][1]:

                    if card[5].y > card[8][1]:
                        card[5].y -= 1 # move card up slightly
                        new_rect = [card[5].x, card[5].y]

                    if card[5].y < card[8][1]:
                        card[5].y += 1 # move card down slightly
                        new_rect = [card[5].x, card[5].y]
            else:
                if card[5].x != new_position[0]:

                    if card[5].x > new_position[0]:
                        card[5].x -= 1 # move card left slightly
                        new_rect = [card[5].x, card[5].y]
                    if card[5].x < new_position[0]:
                        card[5].x += 1 # move card right slightly
                        new_rect = [card[5].x, card[5].y]

                if card[5].y != new_position[1]:

                    if card[5].y > new_position[1]:
                        card[5].y -= 1 # move card up slightly
                        new_rect = [card[5].x, card[5].y]

                    if card[5].y < new_position[1]:
                        card[5].y += 1 # move card down slightly
                        new_rect = [card[5].x, card[5].y]
            i += 1
        # Find and replace old_pos in objects we want to display with the new position
        # change positions of objects on screen
        # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        display.Display.modify_objects_to_display(self, start_rect, new_rect, False)
    #                         obj_to_display
    def sort_card_positions(self, cards, player_cards, pc_cards):
        # PC
        pc_left_padding = 500
        pc_spaces = 200
        new_card_positions_pc = []
        # Defines spacing ranges for pc cards
        i = 0
        # Times Two used because including base card positions
        while i < len(self.pc_cards) * 2:
            if len(self.pc_cards) * 2 <= 6:
                pc_left_padding += 50 # The more cards, the less padding there is from the left side of the screen
                pc_spaces += 5 # The more cards, the smaller spaces in-between
            else:
                pc_left_padding -= 40 # The more cards, the less padding there is from the left side of the screen
                pc_spaces -= 5 # The more cards, the smaller spaces in-between
            # Sets positions for pc cards
            if i == 0:
                pos1 = [500, 150]
                pos1[0] += i * pc_left_padding  # Adjust the x-coordinate based on the index and left padding
                new_card_positions_pc.append(pos1.copy())
            else:
                prev_pos = new_card_positions_pc[i - 1]
                new_pos = [prev_pos[0] + pc_spaces, prev_pos[1]]  # Increment x-coordinate by spaces
                new_card_positions_pc.append(new_pos.copy())
            i += 1
        # PLAYER
        player_left_padding = 500
        player_spaces = 200
        new_card_positions_player = []
        # Defines spacing ranges for pc cards
        i = 0
        # Times Two used because including base card positions
        while i < len(self.player_cards) * 2:
            if len(self.player_cards) * 2 <= 6:
                player_left_padding += 50 # The more cards, the less padding there is from the left side of the screen
                player_spaces += 5 # The more cards, the smaller spaces in-between
            else:
                player_left_padding -= 40 # The more cards, the less padding there is from the left side of the screen
                player_spaces -= 5 # The more cards, the smaller spaces in-between
            # Sets positions for pc cards
            if i == 0:
                pos1 = [500, 650]
                pos1[0] += i * player_left_padding  # Adjust the x-coordinate based on the index and left padding
                new_card_positions_player.append(pos1.copy())
            else:
                prev_pos = new_card_positions_player[i - 1]
                new_pos = [prev_pos[0] + player_spaces, prev_pos[1]]  # Increment x-coordinate by spaces
                new_card_positions_player.append(new_pos.copy())
            i += 1
        # Return list with 2 sublists: player card positions and pc card positions
        return [new_card_positions_player, new_card_positions_pc]

    def move_card_to_new_pos(self, card, new_position):
        i = 0
        start_rect = [card[5][0], card[5][1]]
        new_rect = [card[5][0], card[5][1]]
        print("MOVING CARD TO NEW POS ANIMATION")
        while i < FAST_SPEED: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
            # First position (x or y) is the place we want to move to, the second position (x or y) is where our card is located
            # Aditionally, in new_positions first [0] is the current loop index, second [0] is the position tuple and [1] is the y value of the position
            # Moves the card slightly up in 5 int increments to simulate a hover effect
            # Get next x and y postion by subtracting, resulting in an end animation that heads straight from point A to point B (not jagged)
            x_smoothed = new_position[0]  - card[5][0]
            y_smoothed = new_position[1] - card[5][1]
            
            # Determine the number of steps for movement (if reesult is zero, then use 1 instead, since we cant divide by zero)
            num_steps = max(abs(x_smoothed), abs(y_smoothed)) if max(abs(x_smoothed), abs(y_smoothed)) != 0 else 1

            # Calculate the step size for each axis
            step_x = x_smoothed / num_steps
            step_y = y_smoothed / num_steps

            # Add the smoothed step to the card's current position
            card[5][0] += step_x
            card[5][1] += step_y

            new_rect = [card[5][0], card[5][1]]

            
            i += 1
        display.Display.modify_objects_to_display(self, start_rect, new_rect, False)

    def card_battle(self, pc_card, player_card, attacking_card):
        if attacking_card == pc_card:
            i = 0
            start_rect = [pc_card[5].x, pc_card[5].y]
            new_rect = [pc_card[5].x, pc_card[5].y]
            distance = math.sqrt((player_card[5].x - pc_card[5].x)**2 + (player_card[5].y - pc_card[5].y)**2) 
            #print(distance)
            min_distance = 5
            while i < FAST_SPEED and distance >= min_distance: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
                # Moves the card slightly up in 5 int increments to simulate a hover effect
                # Get next x and y postion by subtracting, resulting in an end animation that heads straight from point A to point B (not jagged)
                x_smoothed = player_card[5].x  - pc_card[5].x
                y_smoothed = player_card[5].y - pc_card[5].y
                
                # Determine the number of steps for movement (if reesult is zero, then use 1 instead, since we cant divide by zero)
                num_steps = max(abs(x_smoothed), abs(y_smoothed)) if max(abs(x_smoothed), abs(y_smoothed)) != 0 else 1

                # Calculate the step size for each axis
                step_x = x_smoothed / num_steps
                step_y = y_smoothed / num_steps

                # Add the smoothed step to the card's current position
                pc_card[5].x += step_x
                pc_card[5].y += step_y

                new_rect = [pc_card[5].x, pc_card[5].y]

                # Calculate distance between first object needs to be within second object to stop
                distance = math.sqrt((player_card[5].x - pc_card[5].x)**2 + (player_card[5].y - pc_card[5].y)**2) 
                
                i += 1
            # Checks and makes sure that only one card image is being displayed on top (not counting base card)
            if True in self.objects_to_display:
                for card in self.objects_to_display:
                    if card[2] is True and start_rect == card[1]:
                        display.Display.modify_objects_to_display(self, start_rect, new_rect, True)
                    else:
                        display.Display.modify_objects_to_display(self, start_rect, new_rect, False)
            else:
                display.Display.modify_objects_to_display(self, start_rect, new_rect, True)
        else:
            i = 0
            start_rect = [player_card[5].x, player_card[5].y]
            new_rect = [player_card[5].x, player_card[5].y]
            distance = math.sqrt((pc_card[5].x - player_card[5].x)**2 + (pc_card[5].y - player_card[5].y)**2) 
            #print(distance)
            min_distance = 0.5
            while i < FAST_SPEED and distance >= min_distance: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
                # Moves the card slightly up in 5 int increments to simulate a hover effect
                # Get next x and y postion by subtracting, resulting in an end animation that heads straight from point A to point B (not jagged)
                x_smoothed = pc_card[5].x  - player_card[5].x
                y_smoothed = pc_card[5].y - player_card[5].y
                
                # Determine the number of steps for movement (if reesult is zero, then use 1 instead, since we cant divide by zero)
                num_steps = max(abs(x_smoothed), abs(y_smoothed)) if max(abs(x_smoothed), abs(y_smoothed)) != 0 else 1

                # Calculate the step size for each axis
                step_x = x_smoothed / num_steps
                step_y = y_smoothed / num_steps

                # Add the smoothed step to the card's current position
                player_card[5].x += step_x
                player_card[5].y += step_y

                new_rect = [player_card[5].x, player_card[5].y]
                # Calculate distance between first object needs to be within second object to stop
                distance = math.sqrt((pc_card[5].x - player_card[5].x)**2 + (pc_card[5].y - player_card[5].y)**2) 
                i += 1
            # Checks and makes sure that only one card image is being displayed on top (not counting base card)
            if True in self.objects_to_display:
                for card in self.objects_to_display:
                    if card[2] is True and start_rect == card[1]:
                        display.Display.modify_objects_to_display(self, start_rect, new_rect, True)
                    else:
                        display.Display.modify_objects_to_display(self, start_rect, new_rect, False)
            else:
                display.Display.modify_objects_to_display(self, start_rect, new_rect, True)
    def card_select(self, card):
        i = 0
        start_rect = [card[5].x, card[5].y]
        while i < FAST_SPEED: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
            # Moves the card slightly up in 5 int increments to simulate a hover effect
            # Get next x and y postion by subtracting, resulting in an end animation that heads straight from point A to point B (not jagged)
            x_smoothed = SELECT_POSITION_X  - card[5].x
            y_smoothed = SELECT_POSITION_Y - card[5].y
            
            # Determine the number of steps for movement (if reesult is zero, then use 1 instead, since we cant divide by zero)
            num_steps = max(abs(x_smoothed), abs(y_smoothed)) if max(abs(x_smoothed), abs(y_smoothed)) != 0 else 1

            # Calculate the step size for each axis
            step_x = x_smoothed / num_steps
            step_y = y_smoothed / num_steps

            # Add the smoothed step to the card's current position
            card[5].x += step_x
            card[5].y += step_y

            new_rect = [card[5].x, card[5].y]
            i += 1
        display.Display.modify_objects_to_display(self, start_rect, new_rect, True)
    def card_select_move(self, card):
        return 1   