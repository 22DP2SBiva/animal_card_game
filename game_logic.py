import random
import card
import utilities
import animations
import round_manager
HOVER_RUN_COUNT = 5
# For handling PC AI strategy and moves
def handle_input(self):
    if self.turn == "PC":
        self.player_battled_all_cards_count = 0 # Reset value
        # Not yet battling
        if self.battling is False:
            # Reset these lists to reuse every frame
            self.shouldnt_attack_cards.clear()
            self.should_attack_cards.clear()
            premature_end_turn = False # If PC should end turn early
            self.card_selected = False # Reset this since there can't be any cards selected
            xtra_points = [] # AI token system (list), tries to battle cards which give it more points
            self.selected_card = None # The card PC is going to battle
            # Checks each card to see which ones higher tier and which to attack
            # Also checks which pc cards have already been attacked, so that we cant attack with those again
            i = 0
            for player_card in self.player_cards:
                for pc_card in self.pc_cards:
                    if pc_card not in self.pc_attacked:  # Check if PC card has already attacked
                        tier_difference = pc_card[1] - player_card[1]
                        if tier_difference >= 0:  # Attack only lower tier or same tier cards
                            points = 3
                        else:
                            points = 0  # Skip attacking higher tier cards
                        # If this player card isnt already going to be attacked, then set to be attacked by this pc card
                        if player_card not in xtra_points:
                            xtra_points.append([points, pc_card, player_card])
                i += 1
            # Sort points by descending, so that PC attacks higher tier cards first and then lower tier, same etc.
            xtra_points.sort(key=lambda x: x[0], reverse=True)  
            # Randomly select a card to attack
            random.shuffle(xtra_points)
            i = 0
            while i < len(xtra_points):
                if xtra_points[i][0] > 0 and self.selected_card is None:  # If points > 0, it means this card should attack now
                    self.selected_card = xtra_points[i][2] # set to player card
                    self.pc_attacked.append(xtra_points[i][1])  # Update list of attacked PC cards
                    current_pc_index = self.pc_cards.index(xtra_points[i][1])
                elif xtra_points[i][0] > 0 and self.selected_card is not None: # This card should attack but not this turn
                    self.should_attack_cards.append(xtra_points[i][1])
                elif xtra_points[i][0] == 0: # This card shouldnt attack at all
                    self.shouldnt_attack_cards.append(xtra_points[i][1])
                i += 1
            # If no card that should attack left, then end turn early
            if len(self.should_attack_cards) == 0 and self.selected_card is None:
                premature_end_turn = True
            i = 0
            if premature_end_turn is False:
                while i < len(self.pc_cards):
                    self.called_battle += 1
                    # Card can be selected, so start battle sequence
                    self.battling = True
                    self.card_shove_sound.play()
                    self.py.event.post(self.battle_event)
                    new_event = self.battle_event
                    # Set the newly posted event as the cards' controlling event
                    self.pc_cards[current_pc_index][11] = new_event
                    self.selected_card[11] = new_event # set player selected card to activate upon battle event
                    self.pc_cards[current_pc_index][15] = True # This card has attacked, so True
                    self.no_cards_attacked_yet = False
                    if self.selected_card is not None:
                        break
                    else:
                        i += 1
            # Should end turn prematurely
            else:
                round_manager.end_turn(self)
        else:
            for cardd in self.pc_cards:
                if cardd[15] is True:
                    self.pc_battled_all_cards_count += 1
                else:
                    self.pc_battled_all_cards_count = 0
            # Battling and not yet deafeated other card
            if self.selected_card is not None:
                self.py.event.post(self.battle_event)
            # Has defeated other card
            elif self.selected_card is None and self.pc_battled_all_cards_count == 0 and premature_end_turn is False:
                self.py.time.delay(500)
                # Sort cards
                utilities.sort_cards(self)
    # Delay first time PC is battling animation for readability
    if self.called_battle == 1:
        self.called_battle += 1
        self.py.time.delay(2000)
    # PLAYER
    elif self.turn == "PLAYER":
        self.player_battled_all_cards_count = 0 # Reset value
        # Collision and animation checks (if generated cards)
        if self.generated_cards and self.card_to_collide is not None:
            for cardd in self.player_cards:
                if not self.battling and not self.combining and cardd[15] == False: # Check if card not in battle mode and not combining
                    # Selecting card when it is hovered over
                    if cardd[6] is True and cardd[12] == self.run_count and self.card_selected is False and cardd[15] is False:
                        if self.pressing:
                            cardd[12] = 0
                            cardd[13] = True
                            # Set that a card is currently selected and which card is currently selected
                            self.card_selected = True
                            self.card_selected_rect = cardd[5]

                            self.py.event.post(self.select_event)
                            cardd[11] = self.select_event
                    # Move selected card when it is NOT hovered over
                    elif cardd[6] is True and cardd[12] != self.run_count and self.card_selected is True and cardd[15] is False:
                        if cardd[5] == self.card_selected_rect:   
                            cardd[12] = 0
                            cardd[13] = True
                            # Set that a card is currently selected and which card is currently selected
                            self.card_selected = True
                            self.card_selected_rect = cardd[5]

                            self.py.event.post(self.select_event)
                            cardd[11] = self.select_event
                    # Hovering over card and not completed animation
                    elif cardd[6] is True and cardd[12] < self.run_count and cardd[15] is False:
                        # Is the mouse being held down?
                        # we are checking if the mouse left click is being pressed and if the currently selected card is not the same as the card being hovered over
                        if self.pressing and self.card_selected is False:
                            cardd[12] = 0
                            cardd[13] = True
                            # Set that a card is currently selected and which card is currently selected
                            self.card_selected = True
                            self.card_selected_rect = cardd[5]
                            self.py.event.post(self.select_event)
                            cardd[11] = self.select_event
                        elif self.pressing is False and self.card_selected is False:
                            self.run_count = HOVER_RUN_COUNT
                            self.py.event.post(self.hover_event)
                            cardd[11] = self.hover_event
                    # If the card is not colliding with anything and the card not selected, then move card back to starting position
                    
                    elif cardd[6] is False and cardd[12] < self.run_count and self.card_selected is False and cardd[13] is False and self.colliding_pc is False and cardd[15] is False:
                        if self.move_back_disabled is False:
                            # [11] is the current event, we are assigning the new event to it
                            self.py.event.post(self.move_to_starting_pos_event)
                            cardd[11] = self.move_to_starting_pos_event
                    # If cursor not collidng with anything but a card has already been selected (and this card is the selcted card)
                    elif cardd[6] is False and cardd[12] < self.run_count and cardd[5] == self.card_selected_rect:
                        if self.battling is False: # If not battling any cards currently
                            cardd[12] = 0
                            cardd[13] = True
                            # Set that a card is currently selected and which card is currently selected
                            self.card_selected = True
                            self.card_selected_rect = cardd[5]

                            self.py.event.post(self.select_event)
                            cardd[11] = self.select_event
                if cardd[15] is True:
                    self.player_battled_all_cards_count += 1
                else:
                    self.player_battled_all_cards_count = 0
    # All these checks and posts have to be made because events have to be posted every frame, otherwise they don't trigger
    # BATTLING CHECK
    if self.battling:
        self.py.event.post(self.battle_event)
    # SORTING CHECK
    if self.sorting_cards and self.done_base_sort:
        self.py.event.post(self.move_to_new_pos_event)
    # COMBINING check
    if self.combining:
        self.py.event.post(self.combine_event)
def finish_combining_cards(self, Card):
    cardd = Card
    cardd[12] = 0
    cardd[16] = True
    self.py.time.delay(500) 
    # Replace first card with higher tier card and remove second to achieve a visual 'combining' appearance
    higher_tier_card = card.generate_higher_tier_card(self.first_card_to_combine[1])
    index = self.player_cards.index(self.first_card_to_combine) # index of fisrt card to combine in player cards list
    obj_to_redefine = self.objects_to_display.index([self.player_cards[index][3], [self.player_cards[index][5].x, self.player_cards[index][5].y], False])
    # Redefine this player cards' values as the higher tiers' ones'
    self.player_cards[index][0] = higher_tier_card[0]
    self.player_cards[index][1] = higher_tier_card[1]
    self.player_cards[index][2] = higher_tier_card[2]
    # convert/scale card image
    self.player_cards[index][3] = self.py.image.load(self.player_cards[index][2])
    self.player_cards[index][3].convert_alpha()
    self.player_cards[index][3] = self.py.transform.scale(self.player_cards[index][3], (1000,900))

    self.player_cards[index][11] = None
    self.player_cards[index][16] = True

    # Redefine card in object list with new values
    self.objects_to_display[obj_to_redefine] = [self.player_cards[index][3], [self.player_cards[index][5].x, self.player_cards[index][5].y], False]
    # Delete second card since we need it to appear that the two cards merge together
    self.player_cards.remove(self.second_card_to_combine)
    self.objects_to_display.remove([self.second_card_to_combine[3], [self.second_card_to_combine[5].x, self.second_card_to_combine[5].y], False])
    # Search in list for base card and remove it
    base_card = utilities.blind_find(self, self.objects_to_display, [self.second_card_to_combine[5].x, self.second_card_to_combine[5].y])
    self.objects_to_display.remove(base_card)
    self.py.time.delay(500)
    # TODO! DO ANIMATION
    self.combine_sound.play()
    
    # Reset values
    self.combining = False
    self.selected_card_count = 0
    self.first_card_to_combine = None
    self.second_card_to_combine = None
    self.card_selected = False
    self.selected_card = None
    self.card_selected_rect = None
    self.combined_cards = True
    self.new_positions = animations.Animations.sort_card_positions(self, self.objects_to_display, self.player_cards, self.pc_cards)
def handle_card_selection(self):
    # PLAYER
    i = 0
    while i < len(self.player_cards):
        # Cursor colliding with player card 
        if self.p_colliding_with_card[i] is True and self.player_cards[i][15] == False:
            # No card selected yet, Select card and place on board
            if self.card_selected is False:
                self.card_place_sound.play()
                self.card_selected = True
                self.card_selected_rect = self.player_cards[i][5]
                self.selected_card = self.player_cards[i]
                self.player_cards[i][11] = self.select_event
                self.py.event.post(self.select_event)
            # Card already selected, 'No.' animation plays
            else:
                if self.card_selected_rect == self.card_to_collide and self.player_cards[i][15] == False:
                    # Cant select same card again
                    self.player_cards[i][11] = self.cant_select_event
                    self.py.event.post(self.cant_select_event)
        i += 1
def combine_cards(self):
    # Select first card
    if self.first_card_to_combine is None:
        self.combining = True

        self.card_selected = True
        self.selected_card = self.first_card_to_combine
        self.card_selected_rect = self.first_card_to_combine

        self.first_card_to_combine = self.card_to_collide
        self.selected_card_count += 1
        self.py.event.post(self.select_event)
        self.first_card_to_combine[11] = self.select_event
    # Selecting same first card (BAD)
    elif self.first_card_to_combine is not None and self.card_to_collide is self.first_card_to_combine:
        # Reset valeus and unselect card
        card_to_change = self.player_cards[self.player_cards.index(self.first_card_to_combine)]
        card_to_change[11] = self.move_to_starting_pos_event
        card_to_change[12] = 0
        card_to_change[15] = False
        card_to_change[13] = False
        card_to_change[6] = False
        self.pressing = False
        self.py.event.post(self.move_to_starting_pos_event)
        self.combining = False

        self.card_selected = False
        self.selected_card = None
        self.card_selected_rect = None

        self.first_card_to_combine = None
        self.selected_card_count = 0
    elif self.card_selected_rect != self.card_to_collide and self.selected_card_count == 1:
        # Set second card as card under cursor
        self.second_card_to_combine = self.card_to_collide
        # Selecting second card (for combining cards)
        # check if theyre the same type of card (Grasshopper for instance)
        if self.first_card_to_combine[1] == self.second_card_to_combine[1] and self.first_card_to_combine[1] is not 4:
            # SELECT BOTH CARDS and COMBINE
            self.selected_card_count += 1 # how many cards have been selected in total
            # Reset selected card since it's about to not exist
            self.card_selected = False
            self.card_selected_rect = None
            
            # Set card events
            self.first_card_to_combine[11] = self.combine_event
            self.second_card_to_combine[11] = self.combine_event
            self.player_cards[self.player_cards.index(self.first_card_to_combine)][11] = self.combine_event
            self.player_cards[self.player_cards.index(self.second_card_to_combine)][11] = self.combine_event
            self.py.event.post(self.combine_event)
            self.current_score += 20
            
        else:
            card_to_change = self.player_cards[self.player_cards.index(self.first_card_to_combine)]
            card_to_change[11] = self.move_to_starting_pos_event
            card_to_change[12] = 0
            card_to_change[15] = False
            card_to_change[13] = False
            card_to_change[6] = False
            self.pressing = False
            self.py.event.post(self.move_to_starting_pos_event)
            # Reset valeus and unselect card
            self.combining = False

            self.card_selected = False
            self.selected_card = None
            self.card_selected_rect = None
            self.second_card_to_combine = None

            self.first_card_to_combine = None
            self.selected_card_count = 0
    elif self.card_selected_rect != self.card_to_collide and self.selected_card_count == 2:
        card_to_change = self.player_cards[self.player_cards.index(self.first_card_to_combine)]
        card_to_change[11] = self.move_to_starting_pos_event
        card_to_change[12] = 0
        card_to_change[15] = False
        card_to_change[13] = False
        card_to_change[6] = False
        
        self.py.event.post(self.move_to_starting_pos_event)
        # Reset valeus and unselect card
        self.combining = False

        self.card_selected = False
        self.selected_card = None
        self.card_selected_rect = None
        self.second_card_to_combine = None
        self.second_card_to_combine = None