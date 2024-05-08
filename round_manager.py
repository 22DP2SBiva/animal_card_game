import card
WHITE = (255, 255, 255)
# For managing rounds/turns
def end_round(self):
    self.sorting_cards = False 
    self.done_base_sort = False
    # END TURN
    self.turn = self.next_turn
    self.display_turn = True
    new_round(self) # Show turn change animation
def end_turn(self):
    if self.turn == "PC":
        self.next_turn = "PLAYER"
        end_round(self)
    elif self.turn == "PLAYER":
        self.next_turn = "PC"
        self.sorting_cards = False 
        self.done_base_sort = False
        # END TURN
        self.turn = self.next_turn
        self.display_turn = True
        new_turn(self)

def reset_card_values(self):
    # Reset variables
    self.battling = False
    self.sorting_cards = False
    self.selected_card = None
    self.card_selected = False
    self.card_selected_rect = None
    self.card_to_collide = False
    self.pc_battled_all_cards_count = 0
    self.player_battled_all_cards_count = 0
    for cardd in self.player_cards:
        cardd[9] = False
        cardd[11] = None # Disable all events for this card
        cardd[12] = 0
        cardd[13] = False
        cardd[15] = False
    for cardd in self.pc_cards:
        cardd[9] = False
        cardd[11] = None # Disable all events for this card
        cardd[12] = 0
        cardd[13] = False
        cardd[15] = False
def soft_reset_card_values(self):
    # Mainly for use in a singular turn since we dont want to reset info about what cards have atacked this turn
    # Reset variables
    self.battling = False
    self.sorting_cards = False
    self.selected_card = None
    self.card_selected = False
    self.card_selected_rect = None
    self.card_to_collide = False
    self.pc_battled_all_cards_count = 0
    self.player_battled_all_cards_count = 0
    for cardd in self.player_cards:
        cardd[9] = False
        cardd[11] = None # Disable all events for this card
        cardd[12] = 0
        cardd[13] = False
    for cardd in self.pc_cards:
        cardd[9] = False
        cardd[11] = None # Disable all events for this card
        cardd[12] = 0
        cardd[13] = False
def new_round(self):
    self.new_round_sound.play()
    self.round_count += 1
    if self.bg_choice == "plains":
        plains = self.py.image.load("Assets/plains.png").convert_alpha()
        self.screen.blit(plains, (0,0))
    elif self.bg_choice == "desert":
        desert = self.py.image.load("Assets/desert.png").convert_alpha()
        self.screen.blit(desert, (0,0))
    else:
        jungle = self.py.image.load("Assets/jungle.png").convert_alpha()
        self.screen.blit(jungle, (0,0))
    
    self.turn_font = self.py.font.SysFont('Arial', 110)
    self.turn_text = self.turn_font.render('Round ' + str(self.round_count), True, (0, 0, 0))
    self.screen.blit(self.turn_text, (750,400))
    # Tier up cards
    card.tier_up_cards(self)
    # UPDATE SCREEN
    self.py.display.update()
    self.clock.tick(60)
    # Delay for 1.2 seconds
    self.py.time.delay(1500) 
    # Show  turn
    if self.turn == "PLAYER":
        self.player_turn_bg = self.py.image.load("Assets/player_turn.png").convert_alpha()
        self.screen.blit(self.player_turn_bg, (0,0))
    else:
        self.pc_turn_bg = self.py.image.load("Assets/pc_turn.png").convert_alpha()
        self.screen.blit(self.pc_turn_bg, (0,0))
    self.py.display.update()
    self.clock.tick(60)
    # Delay for 1.2 seconds
    self.py.time.delay(1800) 
    # Reset variables
    reset_card_values(self)
    self.added_new_cards = False # As we have not yet added a new card this round, set False
    self.already_sorted_at_start = False # Havent sorted cards at start yet
    # Disable this animation
    self.display_turn = False
def new_turn(self):
    self.turn_sound.play()
    self.turn_count += 1
    if self.turn == "PLAYER":
        self.player_turn_bg = self.py.image.load("Assets/player_turn.png").convert_alpha()
        self.screen.blit(self.player_turn_bg, (0,0))
    else:
        self.pc_turn_bg = self.py.image.load("Assets/pc_turn.png").convert_alpha()
        self.screen.blit(self.pc_turn_bg, (0,0))
    # Reset list of pc cards that have already attacked (since it's a new turn and nothing has attacked yet)
    self.pc_attacked.clear()
    soft_reset_card_values(self)
    # UPDATE SCREEN
    self.py.display.update()
    self.clock.tick(60)
    # Delay for 1.2 seconds
    self.py.time.delay(1200) 
    for cardd in self.player_cards:
        cardd[9] = False
        cardd[11] = None # Disable all events for this card
        cardd[12] = 0
        cardd[13] = False
    for cardd in self.pc_cards:
        cardd[9] = False
        cardd[11] = None # Disable all events for this card
        cardd[12] = 0
        cardd[13] = False
    # Disable this animation
    self.display_turn = False
def reset_events(self):
    for cardd in self.player_cards:
        cardd[11] = None
    for cardd in self.pc_cards:
        cardd[11] = None