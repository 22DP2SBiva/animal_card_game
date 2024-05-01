import sys
import math
import random
import pygame
import card
import collisions
import animations
import display
import battle_logic
import file_manager
import screens
import utilities
import text_input
import ui_collision
# dependencies: pygame

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
UNSELECTABLE = 180

HOVER_RUN_COUNT = 5
SELECT_POSITION_X = 900
SELECT_POSITION_Y = 420

PLAYER_CARD_POS_X = 500
PLAYER_CARD_POS_Y = 680
PC_CARD_POS_X = 500
PC_CARD_POS_Y = 150
CARD_SPACING = 220

player_last_card_pos = [0,0] # position of last card in player deck
pc_last_card_pos = [0,0] # position of last card in pc deck
running = True # for checking if game should be running
card_obj = card.Card # import card object

# Objects that should be displayed on the screen
class Game:
    objects_to_display = [] # image(surface), position(list)
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        # Get current monitor size and set screen resolution to that value
        monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h] 
        self.screen = pygame.display.set_mode((monitor_size[0], monitor_size[1]), pygame.FULLSCREEN)

        pygame.display.set_caption("Wildcards")

        self.title_font = pygame.font.SysFont('Arial', 50)

        self.clock = pygame.time.Clock()

        pygame.mixer.init()

        self.py = pygame # For other classes to refrence outside of this class

        # Events (mostly for animations)
        self.hover_e = pygame.USEREVENT + 1
        self.move_to_starting_pos_e = pygame.USEREVENT + 2
        self.select_e = pygame.USEREVENT + 3
        self.cant_select_e = pygame.USEREVENT + 4
        self.battle_e = pygame.USEREVENT + 5
        self.make_selectable_e = pygame.USEREVENT + 6
        self.move_to_new_pos_e = pygame.USEREVENT + 7
        self.combine_e = pygame.USEREVENT + 8

        self.hover_event = pygame.event.Event(self.hover_e)
        self.move_to_starting_pos_event = pygame.event.Event(self.move_to_starting_pos_e)
        self.select_event = pygame.event.Event(self.select_e)
        self.cant_select_event = pygame.event.Event(self.cant_select_e)
        self.battle_event = pygame.event.Event(self.battle_e)
        self.make_selectable_event = pygame.event.Event(self.make_selectable_e)
        self.move_to_new_pos_event = pygame.event.Event(self.move_to_new_pos_e)
        self.combine_event = pygame.event.Event(self.combine_e)

        # Animation handling variables
        self.animated_count = 0
        self.colliding = False # is the cursor colliding with a card?
        self.run_count = 230 # how many frames the animation should run for


        # Booleans to track current screen state
        self.start_screen_active = True
        self.play_screen_active = False
        self.win_screen_active = False
        self.lose_screen_active = False
        self.loading = False

        self.displaying = False
        self.first_round = True
        self.turn = "PLAYER" # Whose turn it is
        self.drawing_unselectable = False # Are we drawing (1) unselectable card already?
        self.colliding_pc = False # Are we colliding with a PC card?
        self.collisions_checked = False
        self.generated_cards = False
        self.shouldnt_attack_cards = [] # Stores which cards shouldnt attack based on strategy
        self.should_attack_cards = []
        self.battled_pc_card = "Brr"
        self.move_back_disabled = False
        self.combining = False
        self.new_positions = [] # If there are any new positions that cards should be moved to, they will be stored in this list
        self.max_card_amount = 6 # first round card amount to deal to each player
        self.debug_mode = False # For debugging (shows all rects)
        self.card_to_collide = None
        # How many live left each player has
        self.player_lives = 5
        self.pc_lives = 5
        self.options_open = False
        self.account_choice_open = False
        self.account_login_open = False
        self.account_signin_open = False
        
        self.round_count = 1 # What round it is numerically?
        self.turn_count = 1
        self.sorted_at_turn_start = False
        self.press_count = 0 # How many times mouse left click has been pressed
        self.pc_attacked = []  # Set to track PC cards that have already attacked
        self.card_selected = False # If a PLAYER card is currently selected to fight, then True
        self.card_selected_rect = None # Currently selected PLAYER card's rect
        self.selected_card = "Brr"# Currently selected PLAYER card
        self.pressing = False # Mouse left button
        self.battling = False # Are two cards currently battling?
        self.next_turn = "PC" # Who's turn is it next?
        self.won = False
        self.lost = False
        self.pc_battled_all_cards_count = 0
        self.player_battled_all_cards_count = 0
        self.no_cards_attacked_yet = True
        self.already_sorted_at_start = False
        self.logged_in = False
        self.user = "Guest"
        self.user_name_text = ""
        self.user_password_text = ""
        self.max_card_count_text = "6"
        self.new_card_count_text = "1"
        self.bg_choice = "plains"
        self.music_volume_text = "20"
        self.sfx_volume_text = "20"
        self.typing_name = False
        self.typing_password = False
        self.typing_max_card_count = False
        self.typing_new_card_count = False
        self.typing_music_volume = False
        self.typing_sfx_volume = False
        
        self.added_new_cards = False # Whether we have added new cards to each deck each turn
        self.selected_card_count = 0 # How many cards are currently selected (for fighting and combining)
        self.player_turn = True # If this round is the player's turn, then True, if pc turn, then False
        self.combined_cards = False # Is the player/pc done combining their cards? each round checked for at the start
        self.sorting_cards = False # If cards are being sorted/ and or moved while sorting, then True
        self.called_battle = 0 # How many times battle event has been called
        self.done_base_sort = False # If cards new positions have been set, then True
        self.display_turn = False # For checking if turn dispaly animation playing
        self.first_card_to_combine = None# First card to combine
        self.second_card_to_combine = None# Second card to combine
        self.options_changed = False
        self.sort_by_high = True

        # Lists
        self.debug_rects = []

        #                  0            1           2                   3                            4            5               6              7                8               9                   10        11          12                  13                  14                      15           16             17
        # list (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating, debug color, current_event, animation_frame_count, move_back_disabled, unselectable_rect, attacked, just_combined)
        self.player_cards = []
        #                  0            1           2                   3                            4            5               6                 7              8             9                  10           11            12               13                  14                      15          16 
        # list (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating, debug color, current_event, animation_frame_count, move_back_disabled, unselectable_rect, attacked)
        self.pc_cards = []

        # Tuples
        self.p_colliding_with_card = ()
        self.pc_colliding_with_card= ()

        

        # IMAGES
        self.end_turn_button = pygame.image.load("Assets/end_turn.png").convert_alpha()
        self.end_turn_button = pygame.transform.scale(self.end_turn_button, (1200,900))

        # SOUNDS
        self.click_sound = pygame.mixer.Sound('Sounds/click.ogg')
        self.toggle_sound = pygame.mixer.Sound('Sounds/toggle.ogg')
        self.switch_sound = pygame.mixer.Sound('Sounds/switch.ogg')
        self.cant_select_sound = pygame.mixer.Sound('Sounds/cant_select.ogg')
        self.new_round_sound = pygame.mixer.Sound('Sounds/new_round.ogg')
        self.cant_select_sound = pygame.mixer.Sound('Sounds/cant_select.ogg')
        self.card_fan_sound = pygame.mixer.Sound('Sounds/cardFan1.ogg')
        self.card_place_sound = pygame.mixer.Sound('Sounds/cardPlace1.ogg')
        self.card_shove_sound = pygame.mixer.Sound('Sounds/cardShove4.ogg')
        self.card_slide_sound = pygame.mixer.Sound('Sounds/cardSlide4.ogg')

        self.music_playing = ""

        
    def generate_cards(self, count_to_generate):
        global player_last_card_pos
        global pc_last_card_pos
        i = 0 # Counter
        x = 0 # Amount by which we move each cards position more
        # Temporary sub-lists
        self.player_sub_list = []
        self.pc_sub_list = []
        
        player_pos = [350, 700] # Default pos
        pc_pos = [350, 80] # Default pos
        # Checks if current turn is not the first, if so then take last card positions from outside and redefine
        if self.turn_count > 1:
            print(self.player_cards)
            player_last_card_pos[0] = self.player_cards[len(self.player_cards)-1][5].x
            player_last_card_pos[1] = self.player_cards[len(self.player_cards)-1][5].y
            pc_last_card_pos[0] = self.pc_cards[len(self.pc_cards)-1][5].x
            pc_last_card_pos[1] = self.pc_cards[len(self.pc_cards)-1][5].y
            player_last_card_pos[0] += 100
            pc_last_card_pos[0] += 100
            player_pos = player_last_card_pos
            pc_pos = pc_last_card_pos
            x = 100
        
        while(i < count_to_generate):
            
            print("i: ", i)
            # Generate card (Name, Tier, Image directory, Ability)
            
            # Create temporary lists that store the values, then add them to the main card deck lists and re-use these temp lists each loop
            # if there's already more than one list in sublists, empty the whole sublist: declare it as empty
            if(len(self.player_sub_list) > 0):  
                self.player_sub_list.clear()
                self.pc_sub_list.clear()
            card_sublist = card.Card.generate_card(self)
            if len(self.player_cards) < self.max_card_amount:
                # generate a card, add it to player deck
                for item in card_sublist:
                    self.player_sub_list.append(item)
            if len(self.pc_cards) < self.max_card_amount:
                # generate a card, add it to pc deck
                card_sublist = card.Card.generate_card(self)
                for item in card_sublist:
                    self.pc_sub_list.append(item)
            if len(self.player_cards) < self.max_card_amount:
                # PLAYER CARDS
                # load/transform card image
                self.player_sub_list[3] = pygame.image.load(self.player_sub_list[2]) # Loads image
                self.player_sub_list[3].convert_alpha() # Removes transparent bits from image
                self.player_sub_list[3] = pygame.transform.scale(self.player_sub_list[3], (1000,900)) # Scales image to fit

                # base cards
                self.player_sub_list.append(pygame.image.load('Assets/b_card.png').convert_alpha())
                self.player_sub_list[4] = pygame.transform.scale(self.player_sub_list[4], (1000,900))
                # create card rects (top left corner = 400+x, 200; widht = 150, height = 300)
                self.player_sub_list.append(pygame.Rect(player_pos[0] + x, player_pos[1], 170, 320)) # start button collsion rect index [5]
                # Add collision check bool
                self.player_sub_list.append(False) # always at start
                # Revealed bool (used for checking if player can currently see waht card it is)
                self.player_sub_list.append(False)
                # add position for further refrencing
                self.player_sub_list.append([player_pos[0] + x, player_pos[1]])
                # animation: is the card curretnly being animated?
                self.player_sub_list.append(False)
                # Color for debug mode
                self.player_sub_list.append(WHITE)
                # Currently activate event for this card
                self.player_sub_list.append(None)
                # Animation frames played in total
                self.player_sub_list.append(0)
                # Can the card move back?
                self.player_sub_list.append(False)
                # Stores refrence to semi-transparent grey image used to display on top of the card, to signify it can't be selected
                self.player_sub_list.append(0)
                # Has the card attacekd?
                self.player_sub_list.append(False)
                # Has the card jsut combined with another card?
                self.player_sub_list.append(False)

                # Store objects which need to be displayed to the screen
                # Base card must be displayed first since it is on the bottom most layer and the card image is on a higher layer
                self.objects_to_display.append([self.player_sub_list[4], self.player_sub_list[8], False])
                self.objects_to_display.append([self.player_sub_list[3], self.player_sub_list[8], False])
            if len(self.pc_cards) < self.max_card_amount:
                print(len(self.pc_cards))
                # PC CARDS
                
                # load card image
                self.pc_sub_list[3] = pygame.image.load(self.pc_sub_list[2])
                self.pc_sub_list[3].convert_alpha()
                self.pc_sub_list[3] = pygame.transform.scale(self.pc_sub_list[3], (1000,900))
                # base cards
                self.pc_sub_list.append(pygame.image.load('Assets/b_card.png').convert_alpha())
                self.pc_sub_list[4] = pygame.transform.scale(self.pc_sub_list[4], (1000,900))

                # Collision rects and checks

                # create card rects (top left corner = 400+x, 200; widht = 150, height = 300)
                self.pc_sub_list.append(pygame.Rect(pc_pos[0] + x, pc_pos[1], 170, 320)) # start button collsion rect index [5]
                # Add collision check bool
                self.pc_sub_list.append(False) # check if cursor is over rect (start button) index [6]
                # Revealed bool (used for checking if player can currently see waht card it is)
                self.pc_sub_list.append(False) # always at start
                # add position for further refrencing
                self.pc_sub_list.append([pc_pos[0] + x, pc_pos[1]])
                # animation: is the card curretnly being animated?
                self.pc_sub_list.append(False)
                # Color for debug mode
                self.pc_sub_list.append(WHITE)
                # Currently activate event for this card
                self.pc_sub_list.append(None)
                # Animation frames played in total
                self.pc_sub_list.append(0)
                # Can the card move back?
                self.pc_sub_list.append(False)
                # Stores refrence to semi-transparent grey image used to display on top of the card, to signify it can't be selected
                self.pc_sub_list.append(0)
                # Has the card attacekd?
                self.pc_sub_list.append(False)
                
                # Store objects which need to be displayed to the screen
                self.objects_to_display.append([self.pc_sub_list[4], self.pc_sub_list[8], False])
                self.objects_to_display.append([self.pc_sub_list[3], self.pc_sub_list[8], False])
            if len(self.player_cards) < self.max_card_amount:
                # append all items in player_sub_list to new empty list ath end of main player_cards list
                self.player_cards.append([])
                new_list = len(self.player_cards) - 1
                y = 0 # for getting rect position
                for item in self.player_sub_list:
                    self.player_cards[new_list].append(item)
                    # Saving positions of last cards to use in next turns
                    if y == 5: # If were at the index the rect should be at, then set last pos to this sublsit value
                        player_last_card_pos[0] = self.player_sub_list[y][0]
                        player_last_card_pos[1] = self.player_sub_list[y][1]
                    y += 1
            if len(self.pc_cards) < self.max_card_amount:
                # append all items in pc_sub_list to main pc_cards list
                self.pc_cards.append([])
                new_list = len(self.pc_cards) - 1
                y = 0 # for getting rect position
                for item in self.pc_sub_list:
                    self.pc_cards[new_list].append(item)
                    # Saving positions of last cards to use in next turns
                    if y == 5: # If were at the index the rect should be at, then set last pos to this sublsit value
                        pc_last_card_pos[0] = self.pc_sub_list[y][0]
                        pc_last_card_pos[1] = self.pc_sub_list[y][1]
                    y += 1
            i += 1
            x += CARD_SPACING
        self.generated_cards = True
        self.added_new_cards = True
    def end_round(self):
        self.sorting_cards = False 
        self.done_base_sort = False
        # END TURN
        self.turn = self.next_turn
        self.display_turn = True
        Game.new_round(self) # Show turn change animation
    def end_turn(self):
        if self.turn == "PC":
            self.next_turn = "PLAYER"
            Game.end_round(self)
        elif self.turn == "PLAYER":
            print("PLAYERR")
            self.next_turn = "PC"
            self.sorting_cards = False 
            self.done_base_sort = False
            # END TURN
            self.turn = self.next_turn
            self.display_turn = True
            Game.new_turn(self)
    def tier_up_cards(self):
        global card_obj
        new_player_card = []
        new_pc_card = []
        old_player_card = []
        old_pc_card = []
        # Replace not top tier cards in original list with next tier card (new cards)
        i = 0
        for cardd in self.player_cards:
            if cardd[1] != 4:
                new_card = card_obj.generate_higher_tier_card(self, cardd[1])
                print("player cards", str(self.player_cards[i]))
                old_player_card.append([self.player_cards[i][3], [self.player_cards[i][5].x, self.player_cards[i][5].y], False])
                self.player_cards[i][0] = new_card[0]
                self.player_cards[i][1] = new_card[1]
                self.player_cards[i][2] = new_card[2]
                # convert/scale card image
                self.player_cards[i][3] = pygame.image.load(new_card[2])
                
                self.player_cards[i][3].convert_alpha()
                self.player_cards[i][3] = pygame.transform.scale(self.player_cards[i][3], (1000,900))
                print("NEW player cards", str(self.player_cards[i]))
                new_player_card.append([self.player_cards[i][3], [self.player_cards[i][5].x, self.player_cards[i][5].y], False])
                
            i += 1
        i = 0
        for cardd in self.pc_cards:
            if cardd[1] != 4:
                new_card = card_obj.generate_higher_tier_card(self, cardd[1])
                old_pc_card.append([self.pc_cards[i][3], [self.pc_cards[i][5].x, self.pc_cards[i][5].y], False])
                self.pc_cards[i][0] = new_card[0]
                self.pc_cards[i][1] = new_card[1]
                self.pc_cards[i][2] = new_card[2]
                # convert/scale card image
                self.pc_cards[i][3] = pygame.image.load(new_card[2])
                self.pc_cards[i][3].convert_alpha()
                self.pc_cards[i][3] = pygame.transform.scale(self.pc_cards[i][3], (1000,900))
                new_pc_card.append([self.pc_cards[i][3], [self.pc_cards[i][5].x, self.pc_cards[i][5].y], False])
                
            i += 1
        i = 0
        for cardd in old_player_card:
            if cardd in self.objects_to_display:
                index = self.objects_to_display.index(cardd)
                self.objects_to_display[index] = new_player_card[i]
            i += 1
        i = 0
        for cardd in old_pc_card:
            if cardd in self.objects_to_display:
                index = self.objects_to_display.index(cardd)
                self.objects_to_display[index] = new_pc_card[i]
            i += 1    
                
        print("last i", i)
    def reset_card_values(self):
        print("Resetting values")
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
        print("Resetting values")
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
        self.round_count += 1
        self.screen.fill(WHITE)
        self.turn_font = pygame.font.SysFont('Arial', 80)
        self.turn_text = self.turn_font.render('Round ' + str(self.round_count), True, (0, 0, 0))
        self.screen.blit(self.turn_text, (750,400))
        # Tier up cards
        Game.tier_up_cards(self)
        # UPDATE SCREEN
        pygame.display.update()
        self.clock.tick(60)
        # Delay for 1.2 seconds
        pygame.time.delay(1200) 
        # Reset variables
        Game.reset_card_values(self)
        self.added_new_cards = False # As we have not yet added a new card this round, set False
        self.already_sorted_at_start = False # Havent sorted cards at start yet
        # Disable this animation
        self.display_turn = False
    def new_turn(self):
        self.turn_count += 1
        self.screen.fill(WHITE)
        self.turn_font = pygame.font.SysFont('Arial', 80)
        self.turn_text = self.turn_font.render(str(self.turn) +'s turn', True, (0, 0, 0))
        self.screen.blit(self.turn_text, (750,400))
        self.turn_num_text = self.turn_font.render(str(self.turn_count), True, (0, 0, 0))
        self.screen.blit(self.turn_num_text, (900,600))
        # Reset list of pc cards that have already attacked (since it's a new turn and nothing has attacked yet)
        self.pc_attacked.clear()
        Game.soft_reset_card_values(self)
        # UPDATE SCREEN
        pygame.display.update()
        self.clock.tick(60)
        # Delay for 1.2 seconds
        pygame.time.delay(1200) 
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
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    def blind_find(self, specified_list, value):
        # Checks list for value and returns the sublist the value is a part of
        # Iterate through the specified list
        for sublist in specified_list:
            # Check if the known value is in the sublist
            if value in sublist:
                # If found, return value
                return sublist
    def sort_cards(self):
        self.sorting_cards = True # Started sorting cards
        # Sort all cards in list position-wise
        self.new_positions = animations.Animations.sort_card_positions(self, self.objects_to_display, self.player_cards, self.pc_cards)
        # Set all cards' current event to moving to new position event
        for cardd in self.player_cards:
            cardd[11] = self.move_to_new_pos_event
        for cardd in self.pc_cards:
            cardd[11] = self.move_to_new_pos_event
        self.done_base_sort = True # Done sorting card position in list
    def reset_events(self):
        for cardd in self.player_cards:
            cardd[11] = None
        for cardd in self.pc_cards:
            cardd[11] = None
    def run(self):
        global running
        while running:
            self.displaying = False # For checking when a new frame was just made
            # ! Make this check EVERY card, not just one and use that for every other list card
            self.pos = pygame.mouse.get_pos() # Cursor position
            # If currently not re-inputting account data, then change current options settings to this accounts settings
            if self.options_open is False:
                if self.typing_name is False and self.typing_password is False:
                    options = file_manager.File_Manager.get_options(self, self.user_name_text, self.user_password_text)
                    print("user", self.user_name_text, self.user_password_text)
                    # Guest user
                    if self.user_name_text == "" and self.user_password_text == "":
                        self.max_card_count_text = options[1][2]
                        self.new_card_count_text = options[1][3]
                        self.bg_choice = options[1][4]
                        self.music_volume_text = options[1][5]
                        self.sfx_volume_text = options[1][6]
                    # Registered user
                    elif self.user_name_text != "" and self.user_password_text != "" and self.options_changed is True:
                        print(options)
                        self.max_card_count_text = options[2]
                        self.new_card_count_text = options[3]
                        self.bg_choice = options[4]
                        self.music_volume_text = options[5]
                        self.sfx_volume_text = options[6]
            if self.display_turn is False and self.won is False and self.lost is False: # If not doing display_turn animation currently
                # COLLISION
                if self.generated_cards: # If card have already been generated
                    
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
                    self.p_colliding_with_card = collisions.Collisions.deck_collide_check(self, self.p_rects, self.p_collission_checks, self.pos) # Player
                    self.pc_colliding_with_card =  collisions.Collisions.deck_collide_check(self, self.pc_rects, self.pc_collission_checks, self.pos) # PC
                    print("Are we combining?", self.combining)
                    self.drawing_unselectable = False # For checking if an unselectable rect is being drawn
                    self.colliding = False
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
                                    pygame.event.post(self.hover_event)
                                    new_event = self.hover_event
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
                                                    pygame.event.post(self.move_to_starting_pos_event)
                                                    new_event = self.move_to_starting_pos_event
                                                    # Set the newly posted event as the cards' controlling event
                                                    self.player_cards[i][11] = new_event    
                                        else:
                                            # If current position of card is not the same as the new position of the card, then move back to new position
                                            if self.player_cards[i][5].x != self.new_positions[0][i][0] or self.player_cards[i][5].y != self.new_positions[0][i][1]:
                                                if self.player_cards[i][13] is False:
                                                    print("NEW POS MOVE BACK")
                                                    if self.move_back_disabled is False: # Check that moving back is not disabled 
                                                        pygame.event.post(self.move_to_starting_pos_event)
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
                                        pygame.event.post(self.battle_event)
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
                                        pygame.event.post(self.cant_select_event)
                                        new_event = self.cant_select_event
                                        # Set the newly posted event as the cards controlling event
                                        self.pc_cards[i][11] = new_event
                                        if self.pc_cards[i][14] != 0:
                                            self.pc_cards[i][14] = 0
                                # If not colliding with this card
                                elif self.pc_colliding_with_card[i] == False:
                                    self.pc_cards[i][9] = False
                                    if self.pc_cards[i][14] != 0:
                                        self.pc_cards[i][14] = 0
                            i += 1
                        self.collisions_checked = True
            
                # START
                # SCREEN MANAGEMENT
                if self.start_screen_active:
                    # If not playing background music, then play
                    if pygame.mixer.music.get_busy() is False or self.music_playing is not "menu":
                        pygame.mixer.music.load('Sounds/menu.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(float(self.music_volume_text)/100)
                        self.music_playing = "menu"
                    screens.Screens.start_screen(self, self.logged_in, self.user)
                if self.options_open:
                    screens.Screens.options_screen(self, self.logged_in, self.user)
                if self.account_choice_open:
                    screens.Screens.account_choice_screen(self, self.logged_in, self.user)
                if self.account_login_open:
                    screens.Screens.account_login_screen(self, self.logged_in, self.user)
                if self.account_signin_open:
                    screens.Screens.account_signin_screen(self, self.logged_in, self.user)
                # PLAY
                if self.play_screen_active:
                    if pygame.mixer.music.get_busy() is False or self.music_playing is not "play1":
                        pygame.mixer.music.load('Sounds/play1.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(float(self.music_volume_text)/100)
                        self.music_playing = "play1"
                    if self.bg_choice == "plains":
                        self.screen.blit(screens.Screens.plains, (0,0))
                    elif self.bg_choice == "desert":
                        self.screen.blit(screens.Screens.desert, (0,0))
                    elif self.bg_choice == "jungle":
                        self.screen.blit(screens.Screens.jungle, (0,0))
                    # End turn button
                    
                    self.screen.blit(self.end_turn_button, (25,850))
                    self.end_turn_button_rect = pygame.Rect(150, 800, 200, 150) # end turn collsion rect
                    self.collide_end_turn_button = self.end_turn_button_rect.collidepoint(self.pos) # check if cursor is over rect (end turn button)
                    # First round
                    if self.round_count == 1 and self.generated_cards == False: # First round and cards have not yet beet generated
                        # PS: self represents instance of the class Game
                        self.generate_cards(self.max_card_amount) # Generate deck of card for both player and pc
                        self.loading = False # Turn off loading screen
                    # Not first round
                    elif self.round_count > 1 and self.added_new_cards == False: # Checks if not first turn and havent already added new cards to each deck
                        self.generate_cards(1) # Generate deck of card for both player and pc
                        self.loading = False
                        self.added_new_cards = True
                    # elif self.round_count > 1 and self.added_new_cards == True and self.sorting_cards == False and self.turn is not "PC":
                    #     if self.sorted_at_turn_start is False:
                    #         print("Sorting as turn start")
                    #         self.sorted_at_turn_start = True
                    #         Game.sort_cards(self) # sort cards before turn start for safety (in case a new card is added)
                # WIN
                elif self.win_screen_active:
                    screens.Screens.win_screen(self)
                # LOSE
                elif self.lose_screen_active:
                    screens.Screens.lose_screen(self)
                # DISPLAY OBJECTS
                display.Display.display_objects(self)
                # DISPLAY DEBUG MODE OBJECTS
                if self.debug_mode:
                    display.Display.debug_draw_rects(self)
                # PC BATTLE AI
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
                                    print("PC tier:", pc_card[1])
                                    print("PLAYER tier:", player_card[1])
                                    if tier_difference >= 0:  # Attack only lower tier or same tier cards
                                        points = 3
                                        print("Tier yes")
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
                        print()
                        print("len xtra", len(xtra_points))
                        print()
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
                        if len(self.should_attack_cards) == 0:
                            premature_end_turn = True
                        i = 0
                        if premature_end_turn is False:
                            while i < len(self.pc_cards):
                                self.called_battle += 1
                                # Card can be selected, so start battle sequence
                                self.battling = True
                                pygame.event.post(self.battle_event)
                                new_event = self.battle_event
                                # Set the newly posted event as the cards' controlling event
                                print("Attacking with", self.pc_cards[i][0])
                                print("Attack ", self.selected_card[0])
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
                            Game.end_turn(self)
                    else:
                        for cardd in self.pc_cards:
                            if cardd[15] is True:
                                self.pc_battled_all_cards_count += 1
                            else:
                                self.pc_battled_all_cards_count = 0
                        # Battling and not yet deafeated other card
                        if self.selected_card is not None:
                            pygame.event.post(self.battle_event)
                        # Has defeated other card
                        elif self.selected_card is None and self.pc_battled_all_cards_count == 0 and premature_end_turn is False:
                            pygame.time.delay(500)
                            # Sort cards
                            print("Sorts cards")
                            Game.sort_cards(self)
                # Delay first time PC is battling animation for readability
                if self.called_battle == 1:
                    self.called_battle += 1
                    print("Delay in called battle")
                    pygame.time.delay(2000)
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
                                        print("Selected 1")
                                        cardd[12] = 0
                                        cardd[13] = True
                                        # Set that a card is currently selected and which card is currently selected
                                        self.card_selected = True
                                        self.card_selected_rect = cardd[5]

                                        pygame.event.post(self.select_event)
                                        cardd[11] = self.select_event
                                # Move selected card when it is NOT hovered over
                                elif cardd[6] is True and cardd[12] != self.run_count and self.card_selected is True and cardd[15] is False:
                                    if cardd[5] == self.card_selected_rect:
                                        print("Selected 1.2")
                                        cardd[12] = 0
                                        cardd[13] = True
                                        # Set that a card is currently selected and which card is currently selected
                                        self.card_selected = True
                                        self.card_selected_rect = cardd[5]

                                        pygame.event.post(self.select_event)
                                        cardd[11] = self.select_event
                                # Hovering over card and not completed animation
                                elif cardd[6] is True and cardd[12] < self.run_count and cardd[15] is False:
                                    # Is the mouse being held down?
                                    # we are checking if the mouse left click is being pressed and if the currently selected card is not the same as the card being hovered over
                                    if self.pressing and self.card_selected is False:
                                        print("Selected 2")
                                        cardd[12] = 0
                                        cardd[13] = True
                                        # Set that a card is currently selected and which card is currently selected
                                        self.card_selected = True
                                        self.card_selected_rect = cardd[5]
                                        pygame.event.post(self.select_event)
                                        cardd[11] = self.select_event
                                    elif self.pressing is False and self.card_selected is False:
                                        print("Hover")
                                        self.run_count = HOVER_RUN_COUNT
                                        pygame.event.post(self.hover_event)
                                        cardd[11] = self.hover_event
                                # If the card is not colliding with anything and the card not selected, then move card back to starting position
                                
                                elif cardd[6] is False and cardd[12] < self.run_count and self.card_selected is False and cardd[13] is False and self.colliding_pc is False and cardd[15] is False:
                                    if self.move_back_disabled is False:
                                        print("Move back to starting position")
                                        # [11] is the current event, we are assigning the new event to it
                                        pygame.event.post(self.move_to_starting_pos_event)
                                        cardd[11] = self.move_to_starting_pos_event
                                # If cursor not collidng with anything but a card has already been selected (and this card is the selcted card)
                                elif cardd[6] is False and cardd[12] < self.run_count and cardd[5] == self.card_selected_rect:
                                    if self.battling is False: # If not battling any cards currently
                                        print("Selected 3")
                                        cardd[12] = 0
                                        cardd[13] = True
                                        # Set that a card is currently selected and which card is currently selected
                                        self.card_selected = True
                                        self.card_selected_rect = cardd[5]

                                        pygame.event.post(self.select_event)
                                        cardd[11] = self.select_event
                            if cardd[15] is True:
                                self.player_battled_all_cards_count += 1
                                print("is true: ", self.player_battled_all_cards_count)
                            else:
                                self.player_battled_all_cards_count = 0
                # All these checks and posts have to be made because events have to be posted every frame, otherwise they don't trigger
                # BATTLING CHECK
                if self.battling:
                    pygame.event.post(self.battle_event)
                # SORTING CHECK
                if self.sorting_cards and self.done_base_sort:
                    pygame.event.post(self.move_to_new_pos_event)
                # COMBINING check
                if self.combining:
                    pygame.event.post(self.combine_event)
                # EVENTS
            for event in pygame.event.get():
                # Close window
                if event.type == pygame.QUIT:
                    print("EXIT GAME QUIT")
                    pygame.quit()
                    sys.exit()
                # For text input
                if event.type == pygame.KEYDOWN:
                    text_input.Text_Input.write_text(self, self.py, event, self.typing_name, self.typing_password, self.typing_max_card_count, self.typing_new_card_count, self.typing_music_volume, self.typing_sfx_volume, self.user_name_text, self.user_password_text, self.max_card_count_text, self.new_card_count_text, self.music_volume_text, self.sfx_volume_text)
                
                # Animations
                # if card hovering called and still should be animating this card, also if currently colliding with something
                if event.type == self.hover_e and self.selected_card_count != 2:
                    for cardd in self.player_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.hover_event:
                            # [12] is the total amount of animation frames that the animation has done
                            print(cardd[12])
                            print(self.run_count)
                            if cardd[12] == self.run_count:
                                # Disable event
                                cardd[12] = 0
                                self.run_count = 230
                            else:
                                animations.Animations.card_hover(self, cardd)
                                cardd[12] += 1
                # if card hovering called and still should be animating this card
                if event.type == self.move_to_starting_pos_e:
                    print("Moving back")
                    i = 0
                    for cardd in self.player_cards:
                        
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.move_to_starting_pos_event:
                            if cardd[12] == self.run_count:
                                # Disable event
                                cardd[12] = 0
                            else:
                                # If no cards have attacked yet and no cards have yet combined, then no positions should be changed (first turn only should apply)
                                if self.no_cards_attacked_yet and self.combined_cards is False:
                                    animations.Animations.move_to_starting_pos(self, cardd, True, None)
                                    cardd[12] += 1
                                elif self.combined_cards:
                                    # If card just combined, move this card above other cards till gets to new position
                                    if cardd[16] is True:
                                        print("\033[31mOLD position\033[0m", [cardd[5].x, cardd[5].y])
                                        print("\033[31mnew position\033[0m", [self.new_positions[0][i][0], self.new_positions[0][i][1] - 50])
                                        animations.Animations.move_to_starting_pos(self, cardd, False, [self.new_positions[0][i][0], self.new_positions[0][i][1] - 50])
                                        if [cardd[5].x, cardd[5].y]  == [self.new_positions[0][i][0], self.new_positions[0][i][1] - 50]: # If card at the new postiiton
                                            cardd[16] = False
                                            print("Yahoo")
                                    else:
                                        print("NOT just combined")
                                        animations.Animations.move_to_starting_pos(self, cardd, False, self.new_positions[0][i])
                                    cardd[12] += 1
                                else:
                                    # Not the first turn
                                    animations.Animations.move_to_starting_pos(self, cardd, False, self.new_positions[0][i])
                                    cardd[12] += 1
                        i += 1
                # Select a card
                if event.type == self.select_e and self.card_selected is True:
                    print("Selecting card")
                    for cardd in self.player_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.select_event:
                            # if card is at the middle of the screen, stop animation
                            if cardd[5].x == SELECT_POSITION_X and cardd[5].y == SELECT_POSITION_Y:
                                # Disable event
                                cardd[12] = 0
                            else:
                                cardd[12] = 1
                                self.card_selected = True
                                animations.Animations.card_select(self, cardd)
                if event.type == self.cant_select_e:
                    # animations.Animations.card_cant_select(self, cardd)
                    for cardd in self.pc_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.cant_select_event:
                            # If there is no card currently selected, then we can't select an enemy card for any reason, so display card as unselectable
                            if self.card_selected is False and self.card_to_collide is cardd:
                                cardd[14] = 1
                    for cardd in self.player_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.cant_select_event:
                            # If there is no card currently selected, then we can't select an enemy card for any reason, so display card as unselectable
                            if self.card_selected is False and self.card_to_collide is cardd:
                                cardd[14] = 1
                if event.type == self.make_selectable_e:
                    print("Make selectable")
                    for cardd in self.pc_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.make_selectable_event:
                            if self.card_selected is True or self.colliding is False:
                                cardd[14] = 0
                                # Disable event
                                cardd[11] = None
                if event.type == self.move_to_new_pos_e:
                    print("Move to NEW POS")
                    self.new_positions = animations.Animations.sort_card_positions(self, self.objects_to_display, self.player_cards, self.pc_cards)
                    i = 0
                    player_cards_reached_pos_count = 0
                    for cardd in self.player_cards: 
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.move_to_new_pos_event:
                            print("Player card moving to NEW POS")
                            # new positions:
                            if cardd[5].x == self.new_positions[0][i][0] and cardd[5].y == self.new_positions[0][i][1]:
                                # Disable event
                                cardd[12] = 0
                                player_cards_reached_pos_count += 1
                            else:
                                self.sorting_cards = True
                                self.done_base_sort = True
                                print("player moving")
                                cardd[12] = 1
                                animations.Animations.move_card_to_new_pos(self, cardd, self.new_positions[0][i])
                            i += 1
                    pc_cards_reached_pos_count = 0
                    i = 0
                    for cardd in self.pc_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.move_to_new_pos_event:
                            print("PC card moving to NEW POS")
                            if cardd[5].x == self.new_positions[1][i][0] and cardd[5].y == self.new_positions[1][i][1]:
                                # Disable event
                                cardd[12] = 0
                                pc_cards_reached_pos_count += 1
                            else:
                                self.sorting_cards = True
                                self.done_base_sort = True
                                print("pc moving")
                                cardd[12] = 1
                                animations.Animations.move_card_to_new_pos(self, cardd, self.new_positions[1][i])
                            i += 1
                    # Checks if all cards have reached the end destination (and all cards for this turn have battled), then end turn
                    if player_cards_reached_pos_count == len(self.player_cards) and pc_cards_reached_pos_count == len(self.pc_cards):
                        self.sorting_cards = False
                        self.card_selected = False
                        self.card_selected_rect = None
                        self.selected_card = None
                        Game.reset_events(self)
                        # All cards have battled this turn, so end turn
                        if self.turn is "PLAYER":
                            print("battled card count:", self.player_battled_all_cards_count)
                            print("player card count", len(self.player_cards))
                            if self.player_battled_all_cards_count == len(self.player_cards):
                                Game.end_turn(self)
                            else:
                                # Hasn't battled all cards yet, so we continue turn and reset values
                                Game.soft_reset_card_values(self)
                                player_cards_reached_pos_count = 0
                                pc_cards_reached_pos_count = 0
                                print("restet player")

                        # All cards have battled this turn, so end turn
                        elif self.turn is "PC":
                            if self.pc_battled_all_cards_count == len(self.pc_cards):
                                Game.end_turn(self)
                            else:
                                # Hasn't battled all cards yet, so we continue turn and reset values
                                Game.soft_reset_card_values(self)
                                print("restet pc")
                                player_cards_reached_pos_count = 0
                                pc_cards_reached_pos_count = 0
                if event.type == self.combine_e:
                    print("Combine")
                    i = 0
                    player_cards_reached_pos_count = 0
                    for cardd in self.player_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.combine_event:
                            print("Combining")
                            min_distance = 15 # minimum distance till "hit" target position
                            # Calculate distance between first and second card
                            distance_to_target = Game.distance(self, self.first_card_to_combine[5].x, self.first_card_to_combine[5].y, self.second_card_to_combine[5].x, self.second_card_to_combine[5].y)
                            if distance_to_target <= min_distance:
                                cardd[12] = 0
                                cardd[16] = True
                                print("Delay in battling")
                                pygame.time.delay(500) 
                                print("before", self.objects_to_display)
                                # Replace first card with higher tier card and remove second to achieve a visual 'combining' appearance
                                higher_tier_card = card.Card.generate_higher_tier_card(self, self.first_card_to_combine[1])
                                index = self.player_cards.index(self.first_card_to_combine) # index of fisrt card to combine in player cards list
                                obj_to_redefine = self.objects_to_display.index([self.player_cards[index][3], [self.player_cards[index][5].x, self.player_cards[index][5].y], False])
                                # Redefine this player cards' values as the higher tiers' ones'
                                print(self.player_cards[index][0])
                                print(higher_tier_card[0])
                                self.player_cards[index][0] = higher_tier_card[0]
                                self.player_cards[index][1] = higher_tier_card[1]
                                self.player_cards[index][2] = higher_tier_card[2]
                                # convert/scale card image
                                self.player_cards[index][3] = pygame.image.load(self.player_cards[index][2])
                                self.player_cards[index][3].convert_alpha()
                                self.player_cards[index][3] = pygame.transform.scale(self.player_cards[index][3], (1000,900))

                                self.player_cards[index][11] = None
                                self.player_cards[index][16] = True

                                # Redefine card in object list with new values
                                print("obj to r", obj_to_redefine)
                                print("in list obj to r", self.objects_to_display[obj_to_redefine])
                                self.objects_to_display[obj_to_redefine] = [self.player_cards[index][3], [self.player_cards[index][5].x, self.player_cards[index][5].y], False]
                                # Delete second card since we need it to appear that the two cards merge together
                                self.player_cards.remove(self.second_card_to_combine)
                                self.objects_to_display.remove([self.second_card_to_combine[3], [self.second_card_to_combine[5].x, self.second_card_to_combine[5].y], False])
                                # Search in list for base card and remove it
                                base_card = Game.blind_find(self, self.objects_to_display, [self.second_card_to_combine[5].x, self.second_card_to_combine[5].y])
                                self.objects_to_display.remove(base_card)
                                print("after", self.objects_to_display)
                                
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

                            else:
                                cardd[12] = 1
                                animations.Animations.combine_cards(self, self.first_card_to_combine, self.second_card_to_combine)
                            i += 1
                if self.turn is "PLAYER":
                    # Display un-selectable cards
                    if self.drawing_unselectable is False:
                        for cardd in self.player_cards:
                            if cardd[14] is not 0:
                                self.drawing_unselectable = True
                                unselectable_image = pygame.Surface(cardd[5].size) # the size of rect
                                unselectable_image.set_alpha(UNSELECTABLE) # alpha level
                                unselectable_image.fill((255,255,255)) # this fills the entire surface
                                self.screen.blit(unselectable_image, [cardd[5].x, cardd[5].y]) # (0,0) are the top-left coordinates
                                # print("DRAWING PLAYER"+ str(cardd))
                        for cardd in self.pc_cards:
                            if cardd[14] is not 0:
                                self.drawing_unselectable = True
                                # print("DRAWING PC" + str(cardd))
                                unselectable_image = pygame.Surface(cardd[5].size) # the size of rect
                                unselectable_image.set_alpha(UNSELECTABLE) # alpha level
                                unselectable_image.fill((255,255,255)) # this fills the entire surface
                                self.screen.blit(unselectable_image, [cardd[5].x, cardd[5].y]) # (0,0) are the top-left coordinates

                # Battle animation
                if event.type == self.battle_e:
                    for cardd in self.pc_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.battle_event:
                            print("Battling")
                            selected_card_pos = [self.selected_card[5].x, self.selected_card[5].y]
                            cardd_pos = [cardd[5].x, cardd[5].y]
                            min_distance = 40 # minimum distance till "hit" target position
                            # Check if it's the PCs' turn, in whick case the PC would be attacking (third parameter is which card is attacking)
                            if self.turn == "PC":
                                # Calculate distance between pc card and player card
                                distance_to_target = Game.distance(self,cardd[5].x, cardd[5].y, self.selected_card[5].x, self.selected_card[5].y)
                                if distance_to_target <= min_distance:
                                    print("Delay in battling")
                                    pygame.time.delay(1000) 
                                    
                                    # Disable event
                                    cardd[12] = 0
                                    self.battled_pc_card = cardd
                                    self.selected_card[12] = 1
                                    # Calculate winner of this battle
                                    winner = battle_logic.Battle_Logic.determine_outcome(self, self.selected_card, cardd)    
                                    if winner == cardd:
                                        print("Remove 1")
                                        if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                            self.player_cards.remove(self.selected_card)
                                            
                                        else:
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                                            self.player_cards.remove(self.selected_card)
                                            
                                        basecard = Game.blind_find(self, self.objects_to_display, selected_card_pos)
                                        self.objects_to_display.remove(basecard)
                                        self.player_lives -= 1
                                        
                                    elif winner is None:
                                        
                                        print("Remove both 2") 
                                        if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                                            if len(self.pc_attacked) > 0:
                                                # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                            self.player_cards.remove(self.selected_card)
                                            
                                        else:
                                             # Remove also card from pc attacked list
                                            # Card is in the list 
                                            if cardd in self.pc_attacked:
                                                self.pc_attacked.remove(cardd)
                                            # Card isnt in list
                                            else:
                                                temp_card = cardd
                                                temp_card[11] = None
                                                # Alternative card is in list
                                                if temp_card in self.pc_attacked:
                                                    self.pc_attacked.remove(temp_card)
                                                # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                                            self.player_cards.remove(self.selected_card)
                                            
                                        basecard = Game.blind_find(self, self.objects_to_display, selected_card_pos)
                                        self.objects_to_display.remove(basecard)
                                        if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                                            
                                            if len(self.pc_attacked) > 0:
                                                # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                                            self.pc_cards.remove(cardd)
                                        else:
                                            # Remove also card from pc attacked list
                                            # Card is in the list 
                                            if cardd in self.pc_attacked:
                                                self.pc_attacked.remove(cardd)
                                            # Card isnt in list
                                            else:
                                                temp_card = cardd
                                                temp_card[11] = None
                                                # Alternative card is in list
                                                if temp_card in self.pc_attacked:
                                                    self.pc_attacked.remove(temp_card)
                                                # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                                            self.pc_cards.remove(cardd)
                                        basecard = Game.blind_find(self, self.objects_to_display, cardd_pos)
                                        self.objects_to_display.remove(basecard)
                                        self.player_lives -= 1
                                        self.pc_lives -= 1
                                    else:
                                        print(self.pc_attacked)
                                        print(cardd)
                                        print("Remove 3") 
                                        if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                                            if len(self.pc_attacked) > 0:
                                                # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                                            self.pc_cards.remove(cardd)
                                        else:
                                            if len(self.pc_attacked) > 0:
                                                # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                                            self.pc_cards.remove(cardd)
                                        basecard = Game.blind_find(self, self.objects_to_display, cardd_pos)
                                        self.objects_to_display.remove(basecard)
                                        self.pc_lives -= 1
                                    pygame.time.delay(500)
                                    # Sort cards
                                    print("Sorts cards")
                                    
                                    Game.sort_cards(self)
                                else:
                                    cardd[12] = 1
                                    self.selected_card[12] = 1
                                    animations.Animations.card_battle(self, cardd, self.selected_card, cardd)
                                
                            # Check if it's the PLAYERS' turn, in whick case the PLAYER would be attacking (third parameter is which card is attacking)
                            elif self.turn == "PLAYER":
                                print("Player battling")
                                distance_to_target = Game.distance(self, self.selected_card[5].x, self.selected_card[5].y, cardd[5].x, cardd[5].y)
                                if distance_to_target <= min_distance:
                                    # Disable event
                                    cardd[12] = 0
                                    self.selected_card[12] = 0
                                    cardd[11] = None
                                    self.selected_card[11] = None
                                    # Calculate winner of this battle
                                    winner = battle_logic.Battle_Logic.determine_outcome(self, cardd, self.selected_card)
                                    # Check which card has won, remove the other card
                                    if winner == cardd:
                                        print("Remove 1") 
                                        
                                        if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                            self.player_cards.remove(self.selected_card)
                                            
                                        else:
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                                            self.player_cards.remove(self.selected_card)
                                            
                                        basecard = Game.blind_find(self, self.objects_to_display, selected_card_pos)
                                        self.objects_to_display.remove(basecard)
                                        self.pc_lives -= 1
                                        
                                    elif winner is None:
                                        
                                        print("Remove both 2") 
                                        if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                                            if len(self.pc_attacked) > 0:
                                            # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                            self.player_cards.remove(self.selected_card)
                                            
                                        else:
                                            if len(self.pc_attacked) > 0:
                                            # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                                            self.player_cards.remove(self.selected_card)
                                            
                                            
                                        basecard = Game.blind_find(self, self.objects_to_display, selected_card_pos)
                                        self.objects_to_display.remove(basecard)
                                        if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                                            if len(self.pc_attacked) > 0:
                                            # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                                            self.pc_cards.remove(cardd)
                                        else:
                                            if len(self.pc_attacked) > 0:
                                            # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                                            self.pc_cards.remove(cardd)
                                        basecard = Game.blind_find(self, self.objects_to_display, cardd_pos)
                                        self.objects_to_display.remove(basecard)
                                        self.player_lives -= 1
                                        self.pc_lives -= 1
                                    else:
                                        print("Remove 3") 
                                        print(self.pc_attacked)
                                        if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                                            if len(self.pc_attacked) > 0:
                                                # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                                            self.pc_cards.remove(cardd)
                                        else:
                                            if len(self.pc_attacked) > 0:
                                                # Remove also card from pc attacked list
                                                # Card is in the list 
                                                if cardd in self.pc_attacked:
                                                    self.pc_attacked.remove(cardd)
                                                # Card isnt in list
                                                else:
                                                    temp_card = cardd
                                                    temp_card[11] = None
                                                    # Alternative card is in list
                                                    if temp_card in self.pc_attacked:
                                                        self.pc_attacked.remove(temp_card)
                                                    # Otherwise card hasnt attacked and isnt in list
                                            self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                                            self.pc_cards.remove(cardd)
                                        basecard = Game.blind_find(self, self.objects_to_display, cardd_pos)
                                        self.objects_to_display.remove(basecard)
                                        self.player_lives -= 1
                                    pygame.time.delay(500)
                                    # Sort cards
                                    print("Sorts cards")
                                    
                                    Game.sort_cards(self)
                                else:
                                    cardd[12] = 1
                                    self.selected_card[12] = 1
                                    animations.Animations.card_battle(self, cardd, self.selected_card, self.selected_card)
                print("Colliding?", self.colliding)
                # Mouse button down (could be any)
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    print("\033[31mPRESSED\033[0m")
                    # LEFT CLICK
                    if event.button == 1 and self.selected_card_count != 1:
                        if self.pressing is False:
                            self.press_count += 1
                            self.pressing = True
                        # START SCREEEN
                        if self.start_screen_active: 
                            print("START")
                            # Start button collision
                            if screens.Screens.collide_start:
                                self.click_sound.play()
                                self.loading = True
                                # Switch to play screen
                                self.start_screen_active = False
                                self.play_screen_active = True
                            if screens.Screens.collide_sort_highest:
                                self.click_sound.play()
                                self.sort_by_high = True
                            if screens.Screens.collide_sort_lowest:
                                self.click_sound.play()
                                self.sort_by_high = False
                        # Open options menu
                        if screens.Screens.collide_options:
                            print("OPTIONS")
                            self.click_sound.play()
                            self.options_open = True
                            self.account_choice_open = False
                            self.start_screen_active = False
                            # Return back to previous screen
                        if self.options_open:
                            if screens.Screens.collide_back:
                                self.switch_sound.play()
                                self.options_open = False
                                self.account_choice_open = False
                                self.account_login_open = False
                                self.account_signin_open = False
                                self.start_screen_active = True
                                screens.Screens.back(self)
                                print("BACK")
                            if screens.Screens.collide_save_options:
                                print("CHANGE OPTIONS")
                                self.new_round_sound.play()
                                file_manager.File_Manager.change_options(self, self.user_name_text, self.user_password_text, self.max_card_count_text, self.new_card_count_text, self.bg_choice, self.music_volume_text, self.sfx_volume_text)
                                screens.Screens.collide_save_options = False
                                if self.user_name_text != "":
                                    self.options_changed = True
                                pygame.mixer.music.set_volume(float(self.music_volume_text)/100)
                                # SAVED text show
                                self.saved_font = pygame.font.SysFont('Arial', 50, True, True)
                                self.saved_surface = self.saved_font.render("SAVED", True, (150,255,150), GREY)
                                self.screen.blit(self.saved_surface, (600, 840))
                                pygame.display.update()
                                pygame.time.delay(500)
                            if screens.Screens.collide_input_max_card:
                                self.toggle_sound.play()
                                self.typing_name = False
                                self.typing_password = False
                                self.typing_max_card_count = True
                                self.typing_new_card_count = False
                                self.typing_music_volume = False
                                self.typing_sfx_volume = False
                            if screens.Screens.collide_input_new_card:
                                self.toggle_sound.play()
                                self.typing_name = False
                                self.typing_password = False
                                self.typing_max_card_count = False
                                self.typing_new_card_count = True
                                self.typing_music_volume = False
                                self.typing_sfx_volume = False
                            if screens.Screens.collide_input_rect_music:
                                self.toggle_sound.play()
                                self.typing_name = False
                                self.typing_password = False
                                self.typing_max_card_count = False
                                self.typing_new_card_count = False
                                self.typing_music_volume = True
                                self.typing_sfx_volume = False
                            if screens.Screens.collide_input_rect_sfx:
                                self.toggle_sound.play()
                                self.typing_name = False
                                self.typing_password = False
                                self.typing_max_card_count = False
                                self.typing_new_card_count = False
                                self.typing_music_volume = False
                                self.typing_sfx_volume = True
                            if screens.Screens.collide_input_rect_bg1:
                                self.toggle_sound.play()
                                self.bg_choice = 'plains'
                            if screens.Screens.collide_input_rect_bg2:
                                self.toggle_sound.play()
                                self.bg_choice = 'desert'
                            if screens.Screens.collide_input_rect_bg3:
                                self.toggle_sound.play()
                                self.bg_choice = 'jungle'
                        # Open account menu
                        if screens.Screens.collide_account:
                            print("ACCOUNT")
                            self.click_sound.play()
                            self.options_open = False
                            self.account_choice_open = True
                            self.start_screen_active = False
                            # Return back to previous screen
                        if screens.Screens.collide_back and self.account_choice_open:
                            self.switch_sound.play()
                            self.options_open = False
                            self.account_choice_open = False
                            self.account_login_open = False
                            self.account_signin_open = False
                            self.start_screen_active = True
                            screens.Screens.back(self)
                            print("BACK")
                        elif screens.Screens.collide_save_options:
                            return 1
                                # file_manager.File_Manager.change_options(self, self.user_name_text, self.user_password, )
                            
                        # Sign in
                        if screens.Screens.collide_signin:
                            self.click_sound.play()
                            self.account_choice_open = False
                            screens.Screens.collide_account = False
                            self.account_signin_open = True
                            self.account_login_open = False
                            screens.Screens.account_signin_screen(self, self.logged_in, self.user)
                        if self.account_signin_open:
                            if screens.Screens.collide_name_input:
                                self.toggle_sound.play()
                                self.typing_name = True
                                self.typing_password = False
                                self.typing_max_card_count = False
                                self.typing_new_card_count = False
                                self.typing_music_volume = False
                                self.typing_sfx_volume = False
                            if screens.Screens.collide_password_input:
                                self.toggle_sound.play()
                                self.typing_name = False
                                self.typing_password = True
                                self.typing_max_card_count = False
                                self.typing_new_card_count = False
                                self.typing_music_volume = False
                                self.typing_sfx_volume = False
                            # Return back to previous screen
                            if screens.Screens.collide_back:
                                self.switch_sound.play()
                                self.options_open = False
                                self.account_choice_open = False
                                self.account_login_open = False
                                self.account_signin_open = False
                                self.start_screen_active = True
                                screens.Screens.back(self)
                                print("BACK")
                            # Pressing save button
                            if screens.Screens.collide_save_account:
                                print("SAVE")
                                self.new_round_sound.play()
                                result = file_manager.File_Manager.add_account(self, self.user_name_text, self.user_password_text)
                                if result == "ACCOUNT ADDED":
                                    self.saved_font = pygame.font.SysFont('Arial', 40, True, True)
                                    self.saved_surface = self.saved_font.render("ADDED ACCOUNT", True, (150,255,150), GREY)
                                    self.screen.blit(self.saved_surface, (660, 830))
                                    pygame.display.update()
                                    pygame.time.delay(500)
                                    self.logged_in = True
                                    self.user = self.user_name_text
                                elif result == "ACCOUNT ALREADY EXISTS":
                                    self.saved_font = pygame.font.SysFont('Arial', 30, True, True)
                                    self.saved_surface = self.saved_font.render("ACCOUNT ALREADY EXISTS", True, (150,255,150), GREY)
                                    self.screen.blit(self.saved_surface, (660, 840))
                                    pygame.display.update()
                                    pygame.time.delay(500)
                                elif result == "EMPTY TEXT":
                                    self.saved_font = pygame.font.SysFont('Arial', 30, True, True)
                                    self.saved_surface = self.saved_font.render("EMPTY", True, (150,255,150), GREY)
                                    self.screen.blit(self.saved_surface, (660, 840))
                                    pygame.display.update()
                                    pygame.time.delay(500)
                                
                        # Log in
                        if screens.Screens.collide_login:
                            print("LOGIN 1st")
                            self.click_sound.play()
                            self.account_choice_open = False
                            screens.Screens.collide_account = False
                            self.account_login_open = True
                            self.account_signin_open = False
                            screens.Screens.account_login_screen(self, self.logged_in, self.user)
                            # Return back to previous screen
                        if self.account_login_open:
                            if screens.Screens.collide_back:
                                self.switch_sound.play()
                                self.options_open = False
                                self.account_choice_open = False
                                self.account_login_open = False
                                self.account_signin_open = False
                                self.start_screen_active = True
                                screens.Screens.back(self)
                                print("BACK T")
                            # Pressing name input text box
                            elif screens.Screens.collide_name_input:
                                self.toggle_sound.play()
                                self.typing_name = True
                                self.typing_password = False
                            # Pressing password input text box
                            elif screens.Screens.collide_password_input:
                                self.toggle_sound.play()
                                self.typing_password = True
                                self.typing_name = False
                            # Pressing login button
                            elif screens.Screens.collide_save_login:
                                print("FILE LOGIN")
                                self.new_round_sound.play()
                                result = file_manager.File_Manager.login(self, self.user_name_text, self.user_password_text)
                                if result == "LOGGED IN":
                                    self.saved_font = pygame.font.SysFont('Arial', 40, True, True)
                                    self.saved_surface = self.saved_font.render("LOGGED IN", True, (150,255,150), GREY)
                                    self.screen.blit(self.saved_surface, (660, 830))
                                    pygame.display.update()
                                    pygame.time.delay(500)
                                    self.logged_in = True
                                    self.user = self.user_name_text
                                elif result == "NO ACCOUNT FOUND":
                                    self.saved_font = pygame.font.SysFont('Arial', 30, True, True)
                                    self.saved_surface = self.saved_font.render("NO ACCOUNT FOUND", True, (150,255,150), GREY)
                                    self.screen.blit(self.saved_surface, (660, 830))
                                    pygame.display.update()
                                    pygame.time.delay(500)
                                
                        # Exit game
                        if screens.Screens.collide_exit:
                            self.click_sound.play()
                            pygame.time.delay(100) # delay exiting so that sound plays
                            print("EXIT GAME")
                            pygame.quit()
                            sys.exit()

                        # Cards have already been generated and collisiosn have been checked earlier
                        if self.generated_cards and self.collisions_checked:
                            print("One")
                            # Cursor colliding with end turn button and clicking (Player wants to end their turn)
                            if self.collide_end_turn_button:
                                print("Colliding with end turn button")
                                Game.end_turn(self)
                            # PLAYER
                            i = 0
                            while i < len(self.player_cards):
                                # Cursor colliding with player card 
                                if self.p_colliding_with_card[i] is True and self.player_cards[i][15] == False:
                                    # No card selected yet, Select card and place on board
                                    if self.card_selected is False:
                                        print("Card selected is False")
                                        self.card_selected = True
                                        self.card_selected_rect = self.player_cards[i][5]
                                        self.selected_card = self.player_cards[i]
                                        self.player_cards[i][11] = self.select_event
                                        pygame.event.post(self.select_event)
                                    # Card already selected, 'No.' animation plays
                                    else:
                                        print("Card selected is True")
                                        if self.card_selected_rect == self.card_to_collide and self.player_cards[i][15] == False:
                                            print("Card selected rect as current rect cursor on")
                                            # Cant select same card again
                                            self.player_cards[i][11] = self.cant_select_event
                                            pygame.event.post(self.cant_select_event)
                                i += 1
                    
                    
                    # RIGHT CLICK
                    elif event.button == 3 and self.card_selected_rect is None:
                        print("Right click")
                        if self.colliding:
                            print("Past colliuding")
                            if self.pressing is False:
                                self.press_count += 1
                                self.pressing = True
                            
                            # Select first card
                            if self.first_card_to_combine is None:
                                print("First card selected")
                                self.combining = True

                                self.card_selected = True
                                self.selected_card = self.first_card_to_combine
                                self.card_selected_rect = self.first_card_to_combine

                                self.first_card_to_combine = self.card_to_collide
                                self.selected_card_count += 1
                                pygame.event.post(self.select_event)
                                self.first_card_to_combine[11] = self.select_event
                            # Selecting same first card (BAD)
                            elif self.first_card_to_combine is not None and self.card_to_collide is self.first_card_to_combine:
                                print(self.card_to_collide)
                                print(self.second_card_to_combine)
                                print("Selecting same first card (NO)")
                                # Reset valeus and unselect card
                                card_to_change = self.player_cards[self.player_cards.index(self.first_card_to_combine)]
                                card_to_change[11] = self.move_to_starting_pos_event
                                card_to_change[12] = 0
                                card_to_change[15] = False
                                card_to_change[13] = False
                                card_to_change[6] = False
                                self.pressing = False
                                pygame.event.post(self.move_to_starting_pos_event)
                                self.combining = False

                                self.card_selected = False
                                self.selected_card = None
                                self.card_selected_rect = None

                                self.first_card_to_combine = None
                                self.selected_card_count = 0
                            elif self.card_selected_rect != self.card_to_collide and self.selected_card_count == 1:
                                # Set second card as card under cursor
                                self.second_card_to_combine = self.card_to_collide
                                print("Not same card and card only 1")
                                # Selecting second card (for combining cards)
                                # check if theyre the same type of card (Grasshopper for instance)
                                if self.first_card_to_combine[1] == self.second_card_to_combine[1] and self.first_card_to_combine[1] is not 4:
                                    print("Combinging!")
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
                                    pygame.event.post(self.combine_event)
                                    
                                else:
                                    print("Not same two cards or Eagles both")
                                    card_to_change = self.player_cards[self.player_cards.index(self.first_card_to_combine)]
                                    card_to_change[11] = self.move_to_starting_pos_event
                                    card_to_change[12] = 0
                                    card_to_change[15] = False
                                    card_to_change[13] = False
                                    card_to_change[6] = False
                                    self.pressing = False
                                    pygame.event.post(self.move_to_starting_pos_event)
                                    # Reset valeus and unselect card
                                    self.combining = False

                                    self.card_selected = False
                                    self.selected_card = None
                                    self.card_selected_rect = None
                                    self.second_card_to_combine = None

                                    self.first_card_to_combine = None
                                    self.selected_card_count = 0
                            elif self.card_selected_rect != self.card_to_collide and self.selected_card_count == 2:
                                print("Not same card and card 2")
                                card_to_change = self.player_cards[self.player_cards.index(self.first_card_to_combine)]
                                card_to_change[11] = self.move_to_starting_pos_event
                                card_to_change[12] = 0
                                card_to_change[15] = False
                                card_to_change[13] = False
                                card_to_change[6] = False
                                
                                pygame.event.post(self.move_to_starting_pos_event)
                                # Reset valeus and unselect card
                                self.combining = False

                                self.card_selected = False
                                self.selected_card = None
                                self.card_selected_rect = None
                                self.second_card_to_combine = None
                                self.second_card_to_combine = None
                                # SHAKE CARD ANIMATION (CANT SELECT ANYMORE)
                            # i = 0
                            # while i < len(self.pc_cards): 
                            #     # Cursor colliding with PC card
                            #     if self.pc_colliding_with_card: # Tuple[bool, rect]
                            #         # Player has selected a card and placed it on the board to fight
                            #         if self.card_selected: # replace with player_cards[8?]
                            #             # If card is already revealed [7], then you can battle it
                            #             if self.pc_cards[7]:
                            #                 break
                            #             # Card is not yet revealed [7], can't battle it
                            #             else:
                            #                 break

                            #         else:
                            #             break
                        #     i += 1
                if event.type == pygame.MOUSEBUTTONUP:
                    self.pressing = False
                    self.press_count = 0
                print("Press count", self.press_count)
                print(pygame.mouse.get_pressed()[0])
                # KEYDOWN events
                if event.type == pygame.KEYDOWN:
                    # Quit game with escape key
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Enter debug mode
                    if event.key == pygame.K_1 and self.play_screen_active:
                        if self.debug_mode == False:
                            self.debug_mode = True
                        else:
                            self.debug_mode = False

            # LOADING SCREEN
            if self.loading:
                self.loading_text = self.title_font.render('Loading', True, (255, 255, 255))
                self.screen.fill(BLACK)
                self.screen.blit(self.loading_text, (870,500))
            if self.generated_cards:
                # WIN/LOSE
                if len(self.player_cards) == 0:
                    screens.Screens.loss_screen(self)
                    self.lost = True
                elif len(self.pc_cards) == 0:
                    screens.Screens.win_screen(self)
                    self.won = True
            self.displaying = True # Set True, because we are about to display a new frame
            # UPDATE SCREEN
            pygame.display.update()
            self.clock.tick(60)
# Run/End game
if running:
    Game().run()
else:
    print("NOT RUNNING EXIT")
    pygame.quit()
    sys.exit()
