import sys
import pygame
import card
import collisions
import animations
import display
# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
running = True # for checking if game should be running
# Objects that should be displayed on the screen
class Game:
    objects_to_display = [] # image(surface), position(tuple)
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Animal card game")

        self.title_font = pygame.font.SysFont('Arial', 50)

        self.clock = pygame.time.Clock()

        # Booleans to track current screen state
        self.start_screen_active = True
        self.play_screen_active = False
        self.win_screen_active = False
        self.lose_screen_active = False
        self.loading = False

        self.first_round = True
        self.collisions_checked = False
        self.generated_cards = False
        self.starting_card_amount = 6 # first round card amount to deal to each player
        self.debug_mode = False # For debugging (shows all rects)

        self.card_selected = False # If a card is currently selected to fight, then True

        # Lists
        self.debug_rects = []

        #                  0            1           2                   3                            4                   5               6              7                8                      9             10        11
        # list (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating, debug color)
        self.player_cards = []
        #                  0            1           2                   3                            4                   5               6                   7              8                   9           10          11
        # list (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating, debug color)
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
            self.player_sub_list.append(pygame.Rect(400+x, 600, 150, 300)) # start button collsion rect index [5]
            # Add collision check bool
            self.player_sub_list.append(False) # always at start
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.player_sub_list.append(False)
            
            # add position for further refrencing
            self.player_sub_list.append([400+x,600])
            # animation: is the card curretnly being animated?
            self.player_sub_list.append(False)
            # Color for debug mode
            self.player_sub_list.append(WHITE)

            # Store objects which need to be displayed to the screen
            self.objects_to_display.append([self.player_sub_list[3], self.player_sub_list[8]])
            self.objects_to_display.append([self.player_sub_list[4], self.player_sub_list[8]])

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
            self.pc_sub_list.append(pygame.Rect(400+x, 200, 150, 300)) # start button collsion rect index [5]
            # Add collision check bool
            self.pc_sub_list.append(False) # check if cursor is over rect (start button) index [6]
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.pc_sub_list.append(False) # always at start
            # add position for further refrencing
            self.pc_sub_list.append([400+x,200])
            # animation: is the card curretnly being animated?
            self.pc_sub_list.append(False)
            # Color for debug mode
            self.pc_sub_list.append(WHITE)
            
            # Store objects which need to be displayed to the screen
            self.objects_to_display.append([self.pc_sub_list[3], self.pc_sub_list[8]])
            self.objects_to_display.append([self.pc_sub_list[4], self.pc_sub_list[8]])

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
            x += 200 
        self.generated_cards = True

    def start_screen(self):
        self.screen.fill(WHITE)
        self.title_text = self.title_font.render('Animal card game', True, (0, 0, 0))
        self.screen.blit(self.title_text, (750,200))
        self.screen.blit(self.start_button, (700,300))
        self.start_rect = pygame.Rect(750, 300, 200, 150) # start button collsion rect
        self.collide_start = self.start_rect.collidepoint(self.pos) # check if cursor is over rect (start button)

        self.screen.blit(self.options_button, (700,500))
        self.screen.blit(self.exit_button, (700,700))
    
    def run(self):
        global running
        while running:
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
                self.p_colliding_with_card = collisions.Collisions.deck_collide_check(self, self.p_rects, self.p_collission_checks, self.pos, self.player_cards) # Player
                self.pc_colliding_with_card =  collisions.Collisions.deck_collide_check(self, self.pc_rects, self.pc_collission_checks, self.pos, self.pc_cards) # PC
                # If colliding with player card, and not curretnyl playing animation play animation Hover (using card rect as parameter)
                # print(self.p_colliding_with_card[0])
                # print(self.p_colliding_with_card[1][9])
                # print(self.p_colliding_with_card[1])
                if self.p_colliding_with_card[0] and self.p_colliding_with_card[1][9] == False:
                    animations.Animations.card_hover(self, self.p_colliding_with_card[1])
                # If colliding with pc card, and not curretnyl playing animation play animation Hover (using card rect as parameter)   
                if self.pc_colliding_with_card[0] and self.pc_colliding_with_card[1][9] == False:
                    animations.Animations.card_hover(self, self.pc_colliding_with_card[1])
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
            # EVENTS
            for event in pygame.event.get():
                # Close window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Mouse down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Cursor colliding with start button
                    if self.collide_start and self.start_screen_active: 
                        self.loading = True
                        # Switch to play screen
                        self.start_screen_active = False
                        self.play_screen_active = True
                    # Cards have already been generated and collisiosn have been checked earlier
                    if self.generated_cards and self.collisions_checked:
                        # PLAYER

                        # Cursor colliding with player card 
                        if self.p_colliding_with_card[0] == True: # Tuple[bool, rect]
                            # No card selected yet, Select card and place on board
                            if self.card_selected == False:
                                break
                            # Card already selected, 'No.' animation plays
                            else:
                                break
                        # PC
                            
                        # Cursor colliding with PC card
                        elif self.pc_colliding_with_card[0] == True: # Tuple[bool, rect]
                            # Player has selected a card and placed it on the board to fight
                            if self.card_selected: # replace with player_cards[8?]
                                # If card is already revealed [7], then you can battle it
                                if self.pc_cards[7]:
                                    break
                                # Card is not yet revealed [7], can't battle it
                                else:
                                    break

                            else:
                                break
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

            # UPDATE SCREEN
            pygame.display.update()
            self.clock.tick(60)
# Run/End game
if running:
    Game().run()
else:
    pygame.quit()
    sys.exit()
