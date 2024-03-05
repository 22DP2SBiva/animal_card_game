import sys
import pygame
import card
import collisions
# Constants
WIDTH, HEIGHT = 1920,1080
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Objects that should be displayed on the screen
objects_to_display = [] # image(surface), position(tuple)
class Game:
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

        self.card_selected = False # If a card is currently selected to fight, then True

        # Lists
        

        #                  0            1           2                   3                            4                   5               6              7                8                      9             10
        # Tuple lists (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating)
        self.player_cards = []
        #                  0            1           2                   3                            4                   5               6                   7              8                   9           10
        # Tuple lists (title(string), tier(int), image dir[string], converted image (surface), ability(string), card base dir[string], rect, collision check bool, card revealed[bool], position[tuple], animating)
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
            card_sublist = card.Card.generate_card()
            # generate a card, add it to player deck
            for item in card_sublist:
                self.player_sub_list.append(item)
            # generate a card, add it to pc deck
            card_sublist = card.Card.generate_card()
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
            self.player_sub_list.append(pygame.Rect(400+x, 200, 150, 300)) # start button collsion rect index [5]
            # Add collision check bool
            self.player_sub_list.append(False) # always at start
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.player_sub_list.append(False)
            
            # add position for further refrencing
            self.player_sub_list.append([400+x,200])
            # animation: is the card curretnly being animated?
            self.player_sub_list.append(False)

            # Store objects which need to be displayed to the screen
            objects_to_display.append([self.player_sub_list[3], self.player_sub_list[8]])
            objects_to_display.append([self.player_sub_list[4], self.player_sub_list[8]])

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
            self.pc_sub_list.append(pygame.Rect(400+x, 600, 150, 300)) # start button collsion rect index [5]
            # Add collision check bool
            self.pc_sub_list.append(False) # check if cursor is over rect (start button) index [6]
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.pc_sub_list.append(False) # always at start
            # add position for further refrencing
            self.pc_sub_list.append([400+x,600])
            # animation: is the card curretnly being animated?
            self.pc_sub_list.append(False)
            # Store objects which need to be displayed to the screen
            objects_to_display.append([self.pc_sub_list[3], self.pc_sub_list[8]])
            objects_to_display.append([self.pc_sub_list[4], self.pc_sub_list[8]])

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
        # TESTING
        self.color = (255, 0, 0) if self.collide_start else (255, 255, 255)
        pygame.draw.rect(self.screen, self.color, self.start_rect)

        # TODO! ADD TO OBJECTS_TO_DISPLAY LIST
        self.screen.blit(self.options_button, (700,500))
        self.screen.blit(self.exit_button, (700,700))
    def display_objects(self):
        # DISPLAYING OBJECTS
        # Display each object to screen
        for object in objects_to_display:
            # Clarification:  image      position
            self.screen.blit(object[0], object[1])
    def modify_objects_to_display(old_value, new_value):
        # Check all items in specified list
        i = 0
        while(i < len(objects_to_display)-1):
            # if the item is the same as the old value were looking for, then replace it as the new value]
            if objects_to_display[i][1] == old_value:
                objects_to_display[i][1] = new_value
            i += 1

    def run(self):
        while True:
            self.pos = pygame.mouse.get_pos() # Cursor position
            # COLLISION
            if (self.generated_cards): # If card have already been generated
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
                # If there's more than one list already in p_rects, remove it and all other lists, because theyre the same length and must exist too then

                self.p_rects = list(map(list, zip(*self.player_cards)))[5] # list of each rect in player cards
                self.p_collission_checks = list(map(list, zip(*self.player_cards)))[6] # list of each collision check (bool) in player cards
                
                self.pc_rects = list(map(list, zip(*self.pc_cards)))[5] # list of each rect in pc cards
                self.pc_collission_checks = list(map(list, zip(*self.pc_cards)))[6] # list of each collision check (bool) in pc cards

                # Goes through each collission check in the list (player cards) and if colliding with cursor then sets them accordingly
                self.p_colliding_with_card = collisions.Collisions.deck_collide_check(self.p_rects, self.p_collission_checks, self.pos, self.player_cards) # Player
                self.pc_colliding_with_card =  collisions.Collisions.deck_collide_check(self.pc_rects, self.pc_collission_checks, self.pos, self.pc_cards) # PC
                # If colliding with player card, and not curretnyl playing animation play animation Hover (using card rect as parameter)
                if(self.p_colliding_with_card[0] and self.p_colliding_with_card[1][9] == False):
                    Animations.card_hover(self, self.p_colliding_with_card[1])
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
            Game.display_objects(self)
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Mouse down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Cursor colliding with start button
                    if (self.collide_start and self.start_screen_active): 
                        self.loading = True
                        # Switch to play screen
                        self.start_screen_active = False
                        self.play_screen_active = True
                    # Cards have already been generated and collisiosn have been checked earlier
                    if(self.generated_cards and self.collisions_checked):
                        # PLAYER

                        # Cursor colliding with player card 
                        if(self.p_colliding_with_card[0] == True): # Tuple[bool, rect]
                            # No card selected yet, Select card and place on board
                            if(self.card_selected == False):
                                break
                            # Card already selected, 'No.' animation plays
                            else:
                                break
                        # PC
                            
                        # Cursor colliding with PC card
                        elif(self.pc_colliding_with_card[0] == True): # Tuple[bool, rect]
                            # Player has selected a card and placed it on the board to fight
                            if(self.card_selected): # replace with player_cards[8?]
                                # If card is already revealed [7], then you can battle it
                                if(self.pc_cards[7]):
                                    break
                                # Card is not yet revealed [7], can't battle it
                                else:
                                    break

                            else:
                                break

                #if event.type == pygame.KEYDOWN:
                #        return
                
            # LOADING SCREEN
            if(self.loading):
                self.loading_text = self.title_font.render('Loading', True, (255, 255, 255))
                self.screen.fill(BLACK)
                self.screen.blit(self.loading_text, (870,500))

            # UPDATE SCREEN
            pygame.display.update()
            self.clock.tick(60)
# ERROR! Make animations work (maybe use a bool to indicate when animation done [maybe add another var to p_cards to know for every single card???])
class Animations:
    """Animates card being hovered over (moves slightly up and stops).

        Parameters:
            image(string): A string(card image directory)
            rect(rect): A rect that's linked to the card
    """
    def card_hover(self, card):
        i = 0
        # Moves the card slightly up in 5 int increments to simulate a hover effect
        while(i < 20):
            old_rect = [card[5].x, card[5].y]
            # Move card slightly up
            card[5].y += 1 # move card up slightly
            new_rect = [card[5].x, card[5].y]
            # Find and replace old_pos in objects we want to display with the new position
            Game.modify_objects_to_display(old_rect, new_rect)
            i += 1
        #ERROR! Fix card collision boxes,
        # also do this:  card animating = true  and replace the card in self.player_cards to the new one
        # check that if card is not being hovered over, then return to original position 
    def card_cant_select(card_rect):
        return 1
    def card_select_move(card_rect):
        return 1   

Game().run()
