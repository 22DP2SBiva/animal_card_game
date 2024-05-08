import sys
import pygame
import collisions
import animations
import display
import battle_logic
import file_manager
import screens
import utilities
import text_input
import game_logic
import round_manager
# dependencies: pygame
# pylint: disable=unsubscriptable-object

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

SELECT_POSITION_X = 900
SELECT_POSITION_Y = 420

PLAYER_CARD_POS_X = 500
PLAYER_CARD_POS_Y = 680
PC_CARD_POS_X = 500
PC_CARD_POS_Y = 150

running = True # for checking if game should be running

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
        self.run_count = 120 # how many frames the animation should run for


        # Booleans to track current screen state
        self.start_screen_active = True
        self.play_screen_active = False
        self.win_screen_active = False
        self.lose_screen_active = False
        self.loading = False

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
        self.press = False
        self.combining = False
        self.new_positions = [] # If there are any new positions that cards should be moved to, they will be stored in this list
        self.max_card_amount = 6 # first round card amount to deal to each player
        self.debug_mode = False # For debugging (shows all rects)
        self.card_to_collide = None
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
        self.current_score = 0
        
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
        self.card_fan_sound = pygame.mixer.Sound('Sounds/cardFan1.ogg')
        self.card_place_sound = pygame.mixer.Sound('Sounds/cardPlace1.ogg')
        self.card_shove_sound = pygame.mixer.Sound('Sounds/cardShove4.ogg')
        self.card_slide_sound = pygame.mixer.Sound('Sounds/cardSlide4.ogg')
        self.combine_sound = pygame.mixer.Sound('Sounds/combine.wav')
        self.turn_sound = pygame.mixer.Sound('Sounds/turn.wav')
        self.card_destroy_sound = pygame.mixer.Sound('Sounds/card_destroy.wav')
        self.sfx_list = [self.click_sound, self.toggle_sound, self.switch_sound, self.cant_select_sound, self.new_round_sound, self.card_fan_sound, self.card_place_sound, self.card_shove_sound, self.card_slide_sound, self.combine_sound, self.turn_sound, self.card_destroy_sound]

        self.music_playing = ""
        
    def run(self):
        global running
        while running:
            # ! Make this check EVERY card, not just one and use that for every other list card
            self.pos = pygame.mouse.get_pos() # Cursor position
            # If currently not re-inputting account data, then change current options settings to this accounts settings
            if self.options_open is False:
                if self.typing_name is False and self.typing_password is False:
                    options = file_manager.File_Manager.get_options(self, self.user_name_text, self.user_password_text)
                    utilities.set_options_values(self, options)
            if self.display_turn is False and self.won is False and self.lost is False: # If not doing display_turn animation currently
                # COLLISION
                if self.generated_cards: # If card have already been generated
                    self.drawing_unselectable = False # For checking if an unselectable rect is being drawn
                    self.colliding = False
                    collisions.check_collisions(self)
                
                screens.screen_management(self)
                
                display.display_objects(self)

                # DISPLAY DEBUG MODE OBJECTS
                if self.debug_mode:
                    display.debug_draw_rects(self)

                # Handles pc and player input checks, decides what the cards should be doing at any moment
                game_logic.handle_input(self)
                
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
                            if cardd[12] >= self.run_count:
                                # Disable event
                                cardd[12] = 0
                                self.run_count = 120
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
                                        # print("\033[31mOLD position\033[0m", [cardd[5].x, cardd[5].y])
                                        # print("\033[31mnew position\033[0m", [self.new_positions[0][i][0], self.new_positions[0][i][1] - 50])
                                        animations.Animations.move_to_starting_pos(self, cardd, False, [self.new_positions[0][i][0], self.new_positions[0][i][1] - 50])
                                        if [cardd[5].x, cardd[5].y]  == [self.new_positions[0][i][0], self.new_positions[0][i][1] - 50]: # If card at the new postiiton
                                            cardd[16] = False
                                    else:
                                        # print("NOT just combined")
                                        animations.Animations.move_to_starting_pos(self, cardd, False, self.new_positions[0][i])
                                    cardd[12] += 1
                                else:
                                    # Not the first turn
                                    animations.Animations.move_to_starting_pos(self, cardd, False, self.new_positions[0][i])
                                    cardd[12] += 1
                        i += 1
                # Select a card
                if event.type == self.select_e and self.card_selected is True:
                    # print("Selecting card")
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
                    # print("Make selectable")
                    for cardd in self.pc_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.make_selectable_event:
                            if self.card_selected is True or self.colliding is False:
                                cardd[14] = 0
                                # Disable event
                                cardd[11] = None
                if event.type == self.move_to_new_pos_e:
                    # print("Move to NEW POS")
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
                        round_manager.reset_events(self)
                        # All cards have battled this turn, so end turn
                        if self.turn is "PLAYER":
                            print("battled card count:", self.player_battled_all_cards_count)
                            print("player card count", len(self.player_cards))
                            if self.player_battled_all_cards_count == len(self.player_cards):
                                round_manager.end_turn(self)
                            else:
                                # Hasn't battled all cards yet, so we continue turn and reset values
                                round_manager.soft_reset_card_values(self)
                                player_cards_reached_pos_count = 0
                                pc_cards_reached_pos_count = 0
                                print("restet player")

                        # All cards have battled this turn, so end turn
                        elif self.turn is "PC":
                            if self.pc_battled_all_cards_count == len(self.pc_cards):
                                round_manager.end_turn(self)
                            else:
                                # Hasn't battled all cards yet, so we continue turn and reset values
                                round_manager.soft_reset_card_values(self)
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
                            min_distance = 3 # minimum distance till "hit" target position
                            # Calculate distance between first and second card
                            distance_to_target = utilities.distance(self.first_card_to_combine[5].x, self.first_card_to_combine[5].y, self.second_card_to_combine[5].x, self.second_card_to_combine[5].y)
                            if distance_to_target <= min_distance:
                                game_logic.finish_combining_cards(self, cardd)
                            else:
                                cardd[12] = 1
                                animations.Animations.combine_cards(self, self.first_card_to_combine, self.second_card_to_combine)
                            i += 1
                display.display_unselectable_cards(self)

                # Battle animation
                if event.type == self.battle_e:
                    for cardd in self.pc_cards:
                        # Is this event the same event the card should be doing?
                        if cardd[11] == self.battle_event:
                            battle_logic.battle(self, cardd)
                self.press = False
                # Mouse button down (could be any)
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    # LEFT CLICK
                    self.press = True
                    if event.button == 1 and self.selected_card_count != 1:
                        if self.pressing is False:
                            self.press_count += 1
                            self.pressing = True
                        screens.handle_selection(self)
                    
                    # RIGHT CLICK
                    elif event.button == 3 and self.card_selected_rect is None:
                        if self.colliding:
                            if self.pressing is False:
                                self.press_count += 1
                                self.pressing = True
                            game_logic.combine_cards(self)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.pressing = False
                    self.press_count = 0
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
            if screens.collide_back_end and self.press:
                screens.reset_game(self)
            # LOADING SCREEN
            if self.loading:
                self.loading_text = self.title_font.render('Loading', True, (255, 255, 255))
                self.screen.fill(BLACK)
                self.screen.blit(self.loading_text, (870,500))
            if self.generated_cards:
                # WIN/LOSE
                if len(self.player_cards) == 0 and len(self.pc_cards) == 0:
                    if pygame.mixer.music.get_busy() is False or self.music_playing is not "draw":
                        pygame.mixer.music.load('Sounds/draw.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(float(self.music_volume_text)/100)
                        self.music_playing = "draw"
                    screens.draw_screen(self)
                    self.lost = True
                elif len(self.player_cards) == 0:
                    if pygame.mixer.music.get_busy() is False or self.music_playing is not "lose":
                        pygame.mixer.music.load('Sounds/lose.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(float(self.music_volume_text)/100)
                        self.music_playing = "lose"
                    screens.loss_screen(self)
                    self.lost = True
                elif len(self.pc_cards) == 0:
                    if pygame.mixer.music.get_busy() is False or self.music_playing is not "win":
                        pygame.mixer.music.load('Sounds/win.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(float(self.music_volume_text)/100)
                        self.music_playing = "win"
                    screens.win_screen(self)
                    self.won = True
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