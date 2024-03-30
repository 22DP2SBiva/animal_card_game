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
        display.Display.modify_objects_to_display(self, start_rect, new_rect, False)
    def move_to_starting_pos(self, card):
        i = 0
        start_rect = [card[5].x, card[5].y]
        while i < SPEED: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
            # Moves card back to the starting position
            # Checks if card current position X is the same as the starting position X
            new_rect = [card[5].x, card[5].y]
            # Checks x and y positions of card and desired position, then moves it accordingly
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
            i += 1
        # Find and replace old_pos in objects we want to display with the new position
        # change positions of objects on screen
        # PS: refrencing self at the start makes it unnecessary to refrence self as a parameter, even if tehnically required (will throw error if you decide to still write it as a parameter too)
        display.Display.modify_objects_to_display(self, start_rect, new_rect, False)
    #                         obj_to_display
    def sort_card_positions(self, cards, player_card_count, pc_card_count):
        # Sort all card positions based on card count, return the new positions
        new_card_positions_player = []
        new_card_positions_pc = []
        width_between_cards = 20  # Adjust as needed
        screen_width = 1920
        screen_height = 1080

        for cardd in cards:
            card_height = cardd[0].get_height()
            card_width = cardd[0].get_width()

            # Calculate total width for player and PC cards
            total_width_player = card_width * player_card_count + width_between_cards * (player_card_count - 1)
            total_width_pc = card_width * pc_card_count + width_between_cards * (pc_card_count - 1)

            # Set minimum padding from the left side of the screen
            min_padding = 100  # Adjust as needed

            # Calculate starting positions for player and PC cards
            start_x_player = max((screen_width - total_width_player) // 2, min_padding)
            start_x_pc = max((screen_width - total_width_pc) // 2, min_padding)

            # Calculate y position for player cards (slightly below middle of the screen)
            player_y = (screen_height // 2) + (screen_height // 10)  # Adjust as needed

            # Calculate y position for PC cards (slightly above middle of the screen)
            pc_y = (screen_height // 2) - (screen_height // 10)  # Adjust as needed

            # Calculate positions for player cards
            for i in range(player_card_count):
                card_x = start_x_player + i * (card_width + width_between_cards)
                new_card_positions_player.append((card_x, player_y))

            # Calculate positions for PC cards
            for i in range(pc_card_count):
                card_x = start_x_pc + i * (card_width + width_between_cards)
                new_card_positions_pc.append((card_x, pc_y - (pc_card_count - 1 - i) * (card_height + 20)))  # Adjust the y position here

        # Return list with 2 sublists: player card positions and pc card positions
        return [new_card_positions_player, new_card_positions_pc]
    def move_card_to_new_pos(self, cards, new_positions):
        i = 0
        while i < 60: # Each loop runs thorugh SPEED times (more speed, the faster the object does the movement)
            for card in cards:
                print(str(new_positions))
                start_rect, new_rect = [card[1][0], card[1][1]]
                # First position (x or y) is the place we want to move to, the second position (x or y) is where our card is located
                # Aditionally, in new_positions first [0] is the current loop index, second [0] is the position tuple and [1] is the y value of the position
                distance = math.sqrt((new_positions[0][0][0] - card[1][0])**2 + (new_positions[0][0][1] - card[1][1])**2) 
                print(distance)
                # Moves the card slightly up in 5 int increments to simulate a hover effect
                # Get next x and y postion by subtracting, resulting in an end animation that heads straight from point A to point B (not jagged)
                
                x_smoothed = new_positions[0][0][0]  - card[1][0]
                y_smoothed = new_positions[0][0][1] - card[1][1]
                
                # Determine the number of steps for movement (if reesult is zero, then use 1 instead, since we cant divide by zero)
                num_steps = max(abs(x_smoothed), abs(y_smoothed)) if max(abs(x_smoothed), abs(y_smoothed)) != 0 else 1

                # Calculate the step size for each axis
                step_x = x_smoothed / num_steps
                step_y = y_smoothed / num_steps

                # Add the smoothed step to the card's current position
                card[1][0] += step_x
                card[1][1] += step_y

                new_rect = [card[1][0], card[1][1]]

                # Calculate distance between first object needs to be within second object to stop
                distance = math.sqrt((new_positions[0][0][0] - card[1][0])**2 + (new_positions[0][0][1] - card[1][1])**2) 
                
                i += 1
                
            display.Display.modify_objects_to_display(self, start_rect, new_rect, True)

    def card_battle(self, pc_card, player_card, attacking_card):
        if attacking_card == pc_card:
            i = 0
            start_rect, new_rect = [pc_card[5].x, pc_card[5].y]
            distance = math.sqrt((player_card[5].x - pc_card[5].x)**2 + (player_card[5].y - pc_card[5].y)**2) 
            print(distance)
            min_distance = 0.5
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
                
            display.Display.modify_objects_to_display(self, start_rect, new_rect, True)
        else:
            i = 0
            start_rect, new_rect = [player_card[5].x, player_card[5].y]
            distance = math.sqrt((pc_card[5].x - player_card[5].x)**2 + (pc_card[5].y - player_card[5].y)**2) 
            print(distance)
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