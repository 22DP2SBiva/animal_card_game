import sys
import pygame
import card
import collisions
import animations
import display
import battle_logic
# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
UNSELECTABLE = 180

HOVER_RUN_COUNT = 5
SELECT_POSITION_X = 900
SELECT_POSITION_Y = 420

PLAYER_CARD_POS_X = 500
PLAYER_CARD_POS_Y = 680
PC_CARD_POS_X = 500
PC_CARD_POS_Y = 150
CARD_SPACING = 160
running = True # for checking if game should be running
# Objects that should be displayed on the screen
class Game:
    objects_to_display = [] # image(surface), position(list)
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption("Wildcards")

        self.title_font = pygame.font.SysFont('Arial', 50)

        self.clock = pygame.time.Clock()

        # Events (mostly for animations)
        self.hover_e = pygame.USEREVENT + 1
        self.move_to_starting_pos_e = pygame.USEREVENT + 2
        self.select_e = pygame.USEREVENT + 3
        self.cant_select_e = pygame.USEREVENT + 4
        self.battle_e = pygame.USEREVENT + 5
        self.make_selectable_e = pygame.USEREVENT + 6

        self.hover_event = pygame.event.Event(self.hover_e)
        self.move_to_starting_pos_event = pygame.event.Event(self.move_to_starting_pos_e)
        self.select_event = pygame.event.Event(self.select_e)
        self.cant_select_event = pygame.event.Event(self.cant_select_e)
        self.battle_event = pygame.event.Event(self.battle_e)
        self.make_selectable_event = pygame.event.Event(self.make_selectable_e)

        # Animation handling variables
        self.animated_count = 0
        self.colliding = False # is the cursor colliding with a card?
        self.run_count = 10 # how many frames the animation should run for


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
        self.battled_pc_card = "Brr"
        self.move_back_disabled = False
        self.starting_card_amount = 6 # first round card amount to deal to each player
        self.debug_mode = False # For debugging (shows all rects)
        self.card_to_collide = None
        self.card_selected = False # If a PLAYER card is currently selected to fight, then True
        self.card_selected_rect = None # Currently selected PLAYER card's rect
        self.selected_card = "Brr"# Currently selected PLAYER card
        self.pressing = False # Mouse left button
        self.battling = False # Are two cards currently battling?
        self.selected_card_count = 0 # How many cards are currently selected (for fighting and combining)
        self.player_turn = True # If this round is the player's turn, then True, if pc turn, then False
        self.combined_cards = False # Is the player/pc done combining their cards? each round checked for at the start
        self.first_card_to_combine = [] # First card to combine
        self.second_card_to_combine = [] # Second card to combine

        # Lists
        self.debug_rects = []

        #                  0            1           2                   3                            4            5               6              7                8               9                   10        11          12                  13                  14                      15
        # list (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating, debug color, current_event, animation_frame_count, move_back_disabled, unselectable_rect)
        self.player_cards = []
        #                  0            1           2                   3                            4            5               6                 7              8             9                  10           11            12               13                  14                      15
        # list (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating, debug color, current_event, animation_frame_count, move_back_disabled, unselectable_rect)
        self.pc_cards = []

        # Tuples
        self.p_colliding_with_card = ()
        self.pc_colliding_with_card= ()

        # IMAGES
        self.start_button = pygame.image.load("Assets/start_button.png").convert_alpha()
        self.options_button = pygame.image.load("Assets/options_button.png").convert_alpha()
        self.exit_button = pygame.image.load("Assets/exit_button.png").convert_alpha()
    def generate_cards(self):
        i = 0 # Counter
        x = 0 # Amount by which we move each cards position more
        # Temporary sub-lists
        self.player_sub_list = []
        self.pc_sub_list = []
        while(i < self.starting_card_amount):
            # Generate card (Name, Tier, Image directory, Ability)

            # Create temporary lists that store the values, then add them to the main card deck lists and re-use these temp lists each loop
            # if there's already more than one list in sublists, empty the whole sublist: declare it as empty
            if(len(self.player_sub_list) > 0):  
                self.player_sub_list.clear()
                self.pc_sub_list.clear()
            card_sublist = card.Card.generate_card(self)
            # generate a card, add it to player deck
            for item in card_sublist:
                self.player_sub_list.append(item)
            # generate a card, add it to pc deck
            card_sublist = card.Card.generate_card(self)
            for item in card_sublist:
                self.pc_sub_list.append(item)
            
            # PLAYER CARDS
            # load/transform card image
            self.player_sub_list[3] = pygame.image.load(self.player_sub_list[2]) # Loads image
            self.player_sub_list[3].convert_alpha() # Removes transparent bits from image
            self.player_sub_list[3] = pygame.transform.scale(self.player_sub_list[3], (800,700)) # Scales image to fit

            # base cards
            self.player_sub_list.append(pygame.image.load('Assets/b_card.png').convert_alpha())
            self.player_sub_list[4] = pygame.transform.scale(self.player_sub_list[4], (800,700))
            # create card rects (top left corner = 400+x, 200; widht = 150, height = 300)
            self.player_sub_list.append(pygame.Rect(PLAYER_CARD_POS_X + x, PLAYER_CARD_POS_Y, 150, 300)) # start button collsion rect index [5]
            # Add collision check bool
            self.player_sub_list.append(False) # always at start
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.player_sub_list.append(False)
            # add position for further refrencing
            self.player_sub_list.append([PLAYER_CARD_POS_X + x,PLAYER_CARD_POS_Y])
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

            # Store objects which need to be displayed to the screen
            # Base card must be displayed first since it is on the bottom most layer and the card image is on a higher layer
            self.objects_to_display.append([self.player_sub_list[4], self.player_sub_list[8], False])
            self.objects_to_display.append([self.player_sub_list[3], self.player_sub_list[8], False])

            # PC CARDS
            
            # load card image
            self.pc_sub_list[3] = pygame.image.load(self.pc_sub_list[2])
            self.pc_sub_list[3].convert_alpha()
            self.pc_sub_list[3] = pygame.transform.scale(self.pc_sub_list[3], (800,700))
            # base cards
            self.pc_sub_list.append(pygame.image.load('Assets/b_card.png').convert_alpha())
            self.pc_sub_list[4] = pygame.transform.scale(self.pc_sub_list[4], (800,700))

            # Collision rects and checks

            # create card rects (top left corner = 400+x, 200; widht = 150, height = 300)
            self.pc_sub_list.append(pygame.Rect(PC_CARD_POS_X + x, PC_CARD_POS_Y, 150, 300)) # start button collsion rect index [5]
            # Add collision check bool
            self.pc_sub_list.append(False) # check if cursor is over rect (start button) index [6]
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.pc_sub_list.append(False) # always at start
            # add position for further refrencing
            self.pc_sub_list.append([PC_CARD_POS_X + x,PC_CARD_POS_Y])
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
            
            # Store objects which need to be displayed to the screen
            self.objects_to_display.append([self.pc_sub_list[4], self.pc_sub_list[8], False])
            self.objects_to_display.append([self.pc_sub_list[3], self.pc_sub_list[8], False])

            # append all items in player_sub_list to new empty list ath end of main player_cards list
            self.player_cards.append([])
            new_list = len(self.player_cards) - 1
            for item in self.player_sub_list:
                self.player_cards[new_list].append(item)
            # append all items in pc_sub_list to main pc_cards list
            self.pc_cards.append([])
            new_list = len(self.pc_cards) - 1
            for item in self.pc_sub_list:
                self.pc_cards[new_list].append(item)
            
            i += 1
            x += CARD_SPACING
        self.generated_cards = True

    def start_screen(self):
        self.screen.fill(WHITE)
        self.title_text = self.title_font.render('Wildcards', True, (0, 0, 0))
        self.screen.blit(self.title_text, (750,200))
        self.screen.blit(self.start_button, (700,300))
        self.start_rect = pygame.Rect(750, 300, 200, 150) # start button collsion rect
        self.collide_start = self.start_rect.collidepoint(self.pos) # check if cursor is over rect (start button)

        self.screen.blit(self.options_button, (700,500))
        self.screen.blit(self.exit_button, (700,700))
    
    def run(self):
        global running
        while running:
            self.displaying = False # For checking when a new frame was just made
            # ! Make this check EVERY card, not just one and use that for every other list card
            self.pos = pygame.mouse.get_pos() # Cursor position
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
                
                self.drawing_unselectable = False # For checking if an unselectable rect is being drawn``
                i = 0
                while i < len(self.p_colliding_with_card):
                    self.player_cards[i][6] = self.p_colliding_with_card[i] # Set colliding bool
                    if self.p_colliding_with_card[i] is True:
                        self.colliding_pc = False
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
                        # if no currently selected card, then animate
                        if self.card_selected is False:
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
                        # If there is no card selected, then move it back to starting position
                        if self.card_selected is False:
                            # If current position of card is not the same as the starting position of the card, then move back to starting position
                            if self.player_cards[i][8] != [self.player_cards[i][5].x,self.player_cards[i][5].y] and self.player_cards[i][13] is False:
                                if self.move_back_disabled is False:
                                    self.colliding = False
                                    pygame.event.post(self.move_to_starting_pos_event)
                                    new_event = self.move_to_starting_pos_event
                                    # Set the newly posted event as the cards' controlling event
                                    self.player_cards[i][11] = new_event     
                        else:   
                            self.colliding = False
                            if self.player_cards[i][14] != 0:
                                self.player_cards[i][14] = 0
                    i += 1
                # Check each pc card, if currently colliding with cursor then sets them accordingly
                i = 0
                while i < len(self.pc_colliding_with_card):
                    # If new collsion check made for this card (i) is True, and not currently animating card, then play animation  
                    print("PC Collisions check: \033[94m" + str(self.pc_colliding_with_card[i]) + " \033[0m")
                    print("PC Animation check: \033[92m" + str(self.pc_cards[i][9]) + " \033[0m")
                    if self.pc_colliding_with_card[i] and self.pc_cards[i][9] == False:
                        self.card_to_collide = self.pc_cards[i]
                        if self.card_selected is True and self.pressing is True:
                            print("Activating battle event")
                            # Card can be selected, so start battle sequence
                            self.battling = True
                            pygame.event.post(self.battle_event)
                            new_event = self.battle_event
                            # Set the newly posted event as the cards' controlling event
                            self.pc_cards[i][11] = new_event
                            self.selected_card[11] = new_event # set player selected card to activate upon battle event
                        elif self.card_selected is False:
                            print("CANT SELECT PC")
                            # Card can't be interacted with, so turn grey
                            pygame.event.post(self.cant_select_event)
                            new_event = self.cant_select_event
                            # Set the newly posted event as the cards' controlling event
                            self.pc_cards[i][11] = new_event
                    # If not colliding with this card
                    elif self.pc_colliding_with_card[i] == False:
                        self.pc_cards[i][9] = False
                        if self.pc_cards[i][14] != 0:
                            self.pc_cards[i][14] = 0
                        # If current position of card is not the same as the starting position of the card, then move back to starting position
                        # ! TODO: TURN BACK TO ORIGINAL COLOR
                    i += 1
                self.collisions_checked = True
           
            # START
            # SCREEN MANAGEMENT
            if(self.start_screen_active):
                self.start_screen()
            # PLAY
            elif(self.play_screen_active):
                self.screen.fill(WHITE)
                if(self.first_round and self.generated_cards == False): # First round and cards have not yet beet generated
                    # PS: self represents instance of the class Game
                    self.generate_cards() # Generate deck of card for both player and pc
                    self.loading = False
            # WIN
            elif(self.win_screen_active):
                return
            # LOSE
            elif(self.lose_screen_active):
                return
            # DISPLAY OBJECTS
            display.Display.display_objects(self)
            # DISPLAY DEBUG MODE OBJECTS
            if self.debug_mode:
                display.Display.debug_draw_rects(self)
            # Collision and animation checks (if generated cards)
            if self.generated_cards and self.card_to_collide is not None:
                for cardd in self.player_cards:
                    if not self.battling: # Check if card in battle mode
                        # Selecting card when it is hovered over
                        if cardd[6] is True and cardd[12] == self.run_count and self.card_selected is False:
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
                        elif cardd[6] is True and cardd[12] != self.run_count and self.card_selected is True:
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
                        elif cardd[6] is True and cardd[12] < self.run_count:
                            # Is the mouse being held down?
                            # we are checking if the mouse left click is being pressed and if the currently selected card is not the same as the card being hovered over
                            if self.pressing and self.card_selected is False or self.card_selected and self.card_selected is False:
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
                        # If the card is not colliding with anything and the card selected is not the same as the current indexed card rect, then move card back to starting position
                        elif cardd[6] is False and cardd[12] < self.run_count and self.card_selected is False and cardd[13] is False and self.colliding_pc is False:
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
            # BATTLING CHECK
            if self.battling:
                pygame.event.post(self.battle_event)
            # EVENTS
            for event in pygame.event.get():
                # Close window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Animations
                # if card hovering called and still should be animating this card, also if currently colliding with something
                if event.type == self.hover_e and self.selected_card_count != 2:
                    for cardd in self.player_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.hover_event:
                            # [12] is the total amount of animation frames that the animation has done
                            if cardd[12] == self.run_count:
                                # Disable event
                                cardd[12] = 0
                            else:
                                animations.Animations.card_hover(self, cardd)
                                cardd[12] += 1
                # if card hovering called and still should be animating this card
                if event.type == self.move_to_starting_pos_e:
                    for cardd in self.player_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.move_to_starting_pos_event:
                            if cardd[12] == self.run_count:
                                # Disable event
                                cardd[12] = 0
                            else:
                                animations.Animations.move_to_starting_pos(self, cardd)
                                cardd[12] += 1
                # Select a card
                if event.type == self.select_e and self.card_selected is True:
                    for cardd in self.player_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.select_event:
                            # if card is at the middle of the screen, stop animation
                            if cardd[5].x == SELECT_POSITION_X and cardd[5].y == SELECT_POSITION_Y:
                                # Disable event
                                cardd[12] = 5
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
                
                # Display un-selectable cards
                if self.drawing_unselectable is False:
                    for cardd in self.player_cards:
                        if cardd[14] is not 0:
                            self.drawing_unselectable = True
                            unselectable_image = pygame.Surface(cardd[5].size) # the size of rect
                            unselectable_image.set_alpha(UNSELECTABLE) # alpha level
                            unselectable_image.fill((255,255,255)) # this fills the entire surface
                            self.screen.blit(unselectable_image, [cardd[5].x, cardd[5].y]) # (0,0) are the top-left coordinates
                            print("DRAWING PLAYER"+ str(cardd))
                    for cardd in self.pc_cards:
                        if cardd[14] is not 0:
                            self.drawing_unselectable = True
                            print("DRAWING PC" + str(cardd))
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
                            # Check if it's the PCs' turn, in whick case the PC would be attacking (third parameter is which card is attacking)
                            if self.turn == "PC":
                                if cardd[5].x == self.selected_card[5].x and cardd[5].y == self.selected_card[5].y:
                                    # Disable event
                                    cardd[12] = 5
                                    self.battled_pc_card = cardd
                                    self.selected_card[12] = 5
                                    # Calculate winner of this battle
                                    winner = battle_logic.Battle_Logic.determine_outcome(self, self.selected_card, cardd)
                                    # Check which card has won, remove the other card
                                    if winner == cardd:
                                        self.objects_to_display.remove(self.selected_card)
                                    elif winner == None:
                                        self.objects_to_display.remove(self.selected_card)
                                        self.objects_to_display.remove(cardd)
                                    else:
                                        self.objects_to_display.remove(cardd)
                                        self.objects_to_display.remove(self.selected_card)
                                    self.battling = False
                                    self.card_selected = False

                                    

                                else:
                                    cardd[12] = 1
                                    self.battled_pc_card = cardd
                                    self.selected_card[12] = 1
                                    animations.Animations.card_battle(self, cardd, self.selected_card, cardd)
                                
                            # Check if it's the PLAYERS' turn, in whick case the PLAYER would be attacking (third parameter is which card is attacking)
                            elif self.turn == "PLAYER":
                                print("Player battling")
                                if self.selected_card[5].x == cardd[5].x and self.selected_card[5].y == cardd[5].y:
                                    # Disable event
                                    cardd[12] = 5
                                    self.selected_card[12] = 5
                                    cardd[11] = None
                                    self.selected_card[11] = None
                                    # Calculate winner of this battle
                                    winner = battle_logic.Battle_Logic.determine_outcome(self, cardd, self.selected_card)
                                    # Check which card has won, remove the other card
                                    if winner == cardd:
                                        print("Remove 1") 
                                        print(self.objects_to_display)
                                        print([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                        print(cardd)
                                        self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                    elif winner is None:
                                        print("Remove both 2") 
                                        print(self.objects_to_display)
                                        print([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                        print([cardd[3], [cardd[5].x, cardd[5].y], False])
                                        self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                                        self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                                    else:
                                        print("Remove 3") 
                                        print(self.objects_to_display)
                                        print([cardd[3], [cardd[5].x, cardd[5].y], False])
                                        print(cardd)
                                        self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                                    

                                else:
                                    cardd[12] = 1
                                    self.selected_card[12] = 1
                                    animations.Animations.card_battle(self, cardd, self.selected_card, cardd)
                # Check if any cards have been deleted, then disable battle mode
                if self.selected_card is None or self.battled_pc_card is None:
                    print("Does this")
                    self.battling = False
                    self.card_selected = False
                    self.move_back_disabled = True
              
                # Mouse button down (could be any)
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    print("\033[31mPRESSED\033[0m")
                    # LEFT CLICK
                    if event.button == 1:
                        self.pressing = True
                        # Cursor colliding with start button
                        if self.collide_start and self.start_screen_active: 
                            self.loading = True
                            # Switch to play screen
                            self.start_screen_active = False
                            self.play_screen_active = True
                        # Cards have already been generated and collisiosn have been checked earlier
                        if self.generated_cards and self.collisions_checked:
                            # PLAYER
                            i = 0
                            while i < len(self.player_cards):
                                # Cursor colliding with player card 
                                if self.p_colliding_with_card[i] is True and self.card_selected and self.card_to_collide != self.card_selected_rect:
                                    # No card selected yet, Select card and place on board
                                    if self.card_selected is False:
                                        pygame.event.post(self.select_event)
                                    # Card already selected, 'No.' animation plays
                                    else:
                                        if self.card_selected_rect == self.card_to_collide:
                                            # Cant select same card again
                                            pygame.event.post(self.cant_select_event)
                                i += 1
                    # RIGHT CLICK
                    elif event.button == 3:
                        self.pressing = True
                        if self.card_selected_rect != self.card_to_collide and self.selected_card_count == 1:
                            # Selecting second card (for combining cards)
                            # check if theyre the same type of card (Grasshopper for instance)
                            if self.first_card_to_combine[1] is self.second_card_to_combine[1]:
                                self.selected_card_count += 1
                                # SELECT BOTH CARDS and COMBINE
                            else:
                                pygame.event.post(self.cant_select_event)
                        elif self.card_selected_rect != self.card_to_collide and self.selected_card_count == 2:
                            break
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
                # KEYDOWN events
                if event.type == pygame.KEYDOWN:
                    # Quit game with escape key
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Enter debug mode
                    if event.key == pygame.K_1:
                        if self.debug_mode == False:
                            self.debug_mode = True
                        else:
                            self.debug_mode = False
            # LOADING SCREEN
            if self.loading:
                self.loading_text = self.title_font.render('Loading', True, (255, 255, 255))
                self.screen.fill(BLACK)
                self.screen.blit(self.loading_text, (870,500))

            self.displaying = True # Set True, because we are about to display a new frame
            # UPDATE SCREEN
            pygame.display.update()
            self.clock.tick(60)
# Run/End game
if running:
    Game().run()
else:
    pygame.quit()
    sys.exit()
