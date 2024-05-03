def deck_collide_check(rects, collision_checks, mouse_pos):
    # Checks for collision between each card in deck and cursor.
    i = 0
    cards_checked = [] # A boolean list to store all cards that have been checked
    while i < len(collision_checks):
        collision_checks[i] = rects[i].collidepoint(mouse_pos)
        if collision_checks[i]: # If cursor colliding with player card
            # return (collision on?, which card this is)
            cards_checked.append(True) # Add True (card colliding with cursor) to list of cards
        else: # Cursors isnt colliding with anything
            cards_checked.append(False) # Add False (card not colliding with cursor) to list of cards
        i += 1
    return cards_checked
def check_collisions(self):
    # These are for easier comprehension of what we are actually putting in the deck_collide_check 
    """ Process:
    We have a list of sub-lists (self.player_cards)
    First we unpack the list and pass it to zip
    The zip then splits the list into tuples which each contain one of the items at the n-th index in every sub-list
    Then we use the map function to turn the tuple array back into a list (because tuples are immutable and we need to be able to change the list values)
    Map returns an interator, so to access the results we need to turn it into a list (again)
    We use list and at the end specify which item in every list we actually want to access (example: the sixth element, so [5])
    Finally, assign it back to the list you want to store those values.
    """

    self.p_rects = list(map(list, zip(*self.player_cards)))[5] # list of each rect in player cards
    self.p_collission_checks = list(map(list, zip(*self.player_cards)))[6] # list of each collision check (bool) in player cards
    
    self.pc_rects = list(map(list, zip(*self.pc_cards)))[5] # list of each rect in pc cards
    self.pc_collission_checks = list(map(list, zip(*self.pc_cards)))[6] # list of each collision check (bool) in pc cards

    # Goes through each collission check in the list (player cards) and if colliding with cursor then sets them accordingly
    self.p_colliding_with_card = deck_collide_check(self.p_rects, self.p_collission_checks, self.pos) # Player
    self.pc_colliding_with_card =  deck_collide_check(self.pc_rects, self.pc_collission_checks, self.pos) # PC

    if self.turn == "PLAYER":
        i = 0
        while i < len(self.p_colliding_with_card):
            self.player_cards[i][6] = self.p_colliding_with_card[i] # Set colliding bool
            if self.p_colliding_with_card[i] is True:
                self.colliding = True
            i += 1
        i = 0
        while i < len(self.pc_colliding_with_card):
            self.pc_cards[i][6] = self.pc_colliding_with_card[i] # Set colliding bool
            if self.pc_colliding_with_card[i] is True:
                self.colliding_pc = True
            i += 1
        # checks each card; If colliding with player card, and not curretnyl playing animation play animation Hover (using card rect as parameter)
        i = 0
        while i < len(self.p_colliding_with_card):
            # If new collsion check made for this card (i) is True, and not currently animating card, then play animation  
            if self.p_colliding_with_card[i] and self.player_cards[i][9] is False:
                self.player_cards[i][9] = True # animation check
                self.player_cards[i][6] = True # collision check
                # if no currently selected card, then animate (and not combining cards)
                if self.card_selected is False and self.combining is False:
                    # So that sorting doesnt overlap hovering at the same time
                    self.selected_card = self.player_cards[i]
                    self.py.event.post(self.hover_event)
                    new_event = self.hover_event
                    if self.player_cards[i][11] is not self.hover_event:
                        self.card_slide_sound.play()
                    # Set the newly posted event as the cards' controlling event
                    self.player_cards[i][11] = new_event
                # Set card to access in animations function (used later) as  the current card being collided with
                self.card_to_collide = self.player_cards[i]
                
            # If not colliding with anything (and selected rect is not this card rect)
            elif self.p_colliding_with_card[i] is False and self.card_selected_rect != self.player_cards[i][5]:
                self.player_cards[i][9] = False # animaton check
                self.player_cards[i][6] = False # collision check
                # If there is no card selected, then move it back to starting position (and not combining cards)
                if self.combining is False:
                    if self.card_selected is False:
                        if self.turn_count == 1:
                            # If current position of card is not the same as the starting position of the card, then move back to starting position
                            if self.player_cards[i][8] != [self.player_cards[i][5].x,self.player_cards[i][5].y] and self.player_cards[i][13] is False:
                                if self.move_back_disabled is False: # Check that moving back is not disabled 
                                    self.py.event.post(self.move_to_starting_pos_event)
                                    new_event = self.move_to_starting_pos_event
                                    # Set the newly posted event as the cards' controlling event
                                    self.player_cards[i][11] = new_event    
                        else:
                            # If current position of card is not the same as the new position of the card, then move back to new position
                            if self.player_cards[i][5].x != self.new_positions[0][i][0] or self.player_cards[i][5].y != self.new_positions[0][i][1]:
                                if self.player_cards[i][13] is False:
                                    print("NEW POS MOVE BACK")
                                    if self.move_back_disabled is False: # Check that moving back is not disabled 
                                        self.py.event.post(self.move_to_starting_pos_event)
                                        new_event = self.move_to_starting_pos_event
                                        # Set the newly posted event as the cards' controlling event
                                        self.player_cards[i][11] = new_event    
                else:
                    if self.player_cards[i][14] != 0:
                        self.player_cards[i][14] = 0
            i += 1
        # Check each pc card, if currently colliding with cursor then sets them accordingly
        i = 0
        while i < len(self.pc_colliding_with_card):
            if self.combining is False:
                # If new collsion check made for this card (i) is True, and not currently animating card, then play animation  
                if self.pc_colliding_with_card[i] and self.pc_cards[i][9] == False:
                    self.card_to_collide = self.pc_cards[i]
                    if self.card_selected is True and self.pressing is True:
                        print("Activating battle event")
                        # Card can be selected, so start battle sequence
                        self.battling = True
                        self.py.event.post(self.battle_event)
                        if self.press:
                            self.card_shove_sound.play()
                        new_event = self.battle_event
                        # Set the newly posted event as the cards controlling event
                        self.pc_cards[i][11] = new_event
                        self.selected_card[11] = new_event # set player selected card to activate upon battle event
                        self.selected_card[15] = True # Is attacking, so True
                        self.no_cards_attacked_yet = False
                        self.player_cards[self.player_cards.index(self.selected_card)][15] = True # Is attacking, so True and set it to player cards too
                    elif self.card_selected is False:
                        print("CANT SELECT PC")
                        # Card can't be interacted with, so turn grey
                        self.py.event.post(self.cant_select_event)
                        new_event = self.cant_select_event
                        # Set the newly posted event as the cards controlling event
                        self.pc_cards[i][11] = new_event
                # If not colliding with this card
                elif self.pc_colliding_with_card[i] == False:
                    self.pc_cards[i][9] = False
            i += 1
        self.collisions_checked = True