# for storing and displaying screens
# pylint: disable=no-member
import sys
import file_manager
import utilities
import round_manager
import game_logic
import card

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
generated_images = False
# Collision checks
collide_start = False
collide_options = False
collide_account = False
collide_exit = False
collide_input_max_card = False
collide_input_new_card = False
collide_input_rect_bg1 = False
collide_input_rect_bg2 = False
collide_input_rect_bg3 = False
collide_input_rect_music = False
collide_input_rect_sfx = False
collide_back = False
collide_save_options = False
collide_login = False
collide_signin = False
collide_back = False
collide_save_login = False
collide_back = False
collide_name_input = False
collide_password_input = False
collide_save_account = False
collide_back = False
collide_back_end = False
collide_password_input = False
collide_sort_highest = False
collide_sort_lowest = False
plains = None
jungle = None
desert = None
def generate_images(self):
    global plains, jungle, desert, generated_images
    plains = self.py.image.load("Assets/plains.png").convert_alpha()
    jungle = self.py.image.load("Assets/jungle.png").convert_alpha()
    desert = self.py.image.load("Assets/desert.png").convert_alpha()
    self.bg_plains = self.py.image.load("Assets/bg_plains.png").convert_alpha()
    self.start_button = self.py.image.load("Assets/start_button.png").convert_alpha()
    self.options_button = self.py.image.load("Assets/options_button.png").convert_alpha()
    self.account_button = self.py.image.load("Assets/account_button.png").convert_alpha()
    self.exit_button = self.py.image.load("Assets/exit_button.png").convert_alpha()
    self.logo = self.py.image.load("Assets/logo.png").convert_alpha()
    self.start_button = self.py.transform.scale(self.start_button, (1200,900))
    self.options_button = self.py.transform.scale(self.options_button, (1200,900))
    self.account_button = self.py.transform.scale(self.account_button, (1200,900))
    self.exit_button = self.py.transform.scale(self.exit_button, (1200,900))
    self.sort_buttons = self.py.image.load("Assets/sort_buttons.png").convert_alpha()
    self.scoreboard_text = self.py.image.load("Assets/scoreboard_text.png").convert_alpha()
    self.score_name_panel = self.py.image.load("Assets/score_name_panel.png").convert_alpha()
    self.score_name_text = self.py.image.load("Assets/score_name_text.png").convert_alpha()
    self.medal1 = self.py.image.load("Assets/medal_1.png").convert_alpha()
    self.medal2 = self.py.image.load("Assets/medal_2.png").convert_alpha()
    self.medal3 = self.py.image.load("Assets/medal_3.png").convert_alpha()
    self.sort_buttons  = self.py.transform.scale(self.sort_buttons, (1200,700))
    self.scoreboard_text = self.py.transform.scale(self.scoreboard_text, (2900,1600))
    self.score_name_panel = self.py.transform.scale(self.score_name_panel, (2900,1600))
    self.score_name_text = self.py.transform.scale(self.score_name_text, (2900,1600))
    self.medal1 = self.py.transform.scale(self.medal1, (1000,600))
    self.medal2 = self.py.transform.scale(self.medal2, (1000,600))
    self.medal3 = self.py.transform.scale(self.medal3, (1000,600))
    self.options_panel = self.py.image.load("Assets/options_panel.png").convert_alpha()
    self.options_panel = self.py.transform.scale(self.options_panel, (1700,1100))
    self.account_choice_panel = self.py.image.load("Assets/account_choice_panel.png").convert_alpha()
    self.account_choice_panel = self.py.transform.scale(self.account_choice_panel, (1700,1100))
    
    self.account_login_panel = self.py.image.load("Assets/login_panel.png").convert_alpha()
    self.account_login_panel = self.py.transform.scale(self.account_login_panel, (1700,1100))
    
    self.account_signin_panel = self.py.image.load("Assets/signup_panel.png").convert_alpha()
    self.account_signin_panel = self.py.transform.scale(self.account_signin_panel, (1700,1100))
    generated_images = True
def display_account(self, logged_in, user):
    # Display account username text at top of screen always
    if logged_in is False:
        user = "Guest"
    # Dispaly and dynamically size text
    size = 50
    for letter in user:
        size -= 2
    self.name_font = self.py.font.SysFont('Arial', size)
    self.name_surface = self.name_font.render(user, True, GREY)
    self.screen.blit(self.name_surface, (1760, 30))
def start_screen(self, logged_in, user):
    global collide_back_end, collide_sort_highest, collide_sort_lowest, collide_start, collide_options, collide_account, collide_exit
    if generated_images is False: # Pre-generate images for later use
        generate_images(self)

    self.screen.blit(self.bg_plains, (0,0))
    collide_back_end = False
    
    self.screen.blit(self.scoreboard_text, (240,410))
    # 3 top players
    self.score_font = self.py.font.SysFont('Arial', 40)

    accounts = file_manager.File_Manager.get_account_data(self, self.user_name_text, self.user_password_text)
    players = []
    if self.sort_by_high is True:
        players = utilities.sort_by_highest(accounts)
    else:
        players = utilities.sort_by_lowest(accounts)
    if players: # If list not empty
        if len(players) == 1:
            self.screen.blit(self.medal1, (170,575))
            size = 50
            # Name sizing
            for letter in players[0][1]:
                size -= 2
            self.name_font = self.py.font.SysFont('Arial', size)

            self.screen.blit(self.score_name_panel, (205,550))
            # Score
            self.score_1 = self.score_font.render(players[0][0], True, (0,0,0))
            self.screen.blit(self.score_1, (265,580))
            # Name
            self.name_1 = self.name_font.render(players[0][1], True, (0,0,0))
            self.screen.blit(self.name_1, (430,580))
        elif 1 < len(players) < 3:
            # Display first two players
            if self.sort_by_high:
                self.screen.blit(self.medal1, (170,575))
                self.screen.blit(self.medal2, (170,650))
            else:
                self.screen.blit(self.medal1, (170,650))
                self.screen.blit(self.medal2, (170,575))
            size = 50
            # Name sizing
            for letter in players[0][1]:
                size -= 2
            self.name_font = self.py.font.SysFont('Arial', size)

            self.screen.blit(self.score_name_panel, (205,550))
            # Score
            self.score_1 = self.score_font.render(players[0][0], True, (0,0,0))
            self.screen.blit(self.score_1, (265,580))
            # Name
            self.name_1 = self.name_font.render(players[0][1], True, (0,0,0))
            self.screen.blit(self.name_1, (430,580))

            
            self.screen.blit(self.score_name_panel, (205,630))
            size = 50
            for letter in players[1][1]:
                size -= 2
            self.name_font = self.py.font.SysFont('Arial', size)

            self.score_2 = self.score_font.render(players[1][0], True, (0,0,0))
            self.screen.blit(self.score_2, (265,660))
            self.name_2 = self.name_font.render(players[1][1], True, (0,0,0))
            self.screen.blit(self.name_2, (430,660))
        else:
            # Sort medals by score
            if self.sort_by_high:
                self.screen.blit(self.medal1, (170,575))
                self.screen.blit(self.medal2, (170,650))
                self.screen.blit(self.medal3, (170,730))
            else: # Sort by lowest score
                if len(players) <= 3:
                    self.screen.blit(self.medal1, (170,730))
                    self.screen.blit(self.medal2, (170,650))
                    self.screen.blit(self.medal3, (170,575))
                elif len(players) == 4:
                    self.screen.blit(self.medal2, (170,730))
                    self.screen.blit(self.medal3, (170,650))
                elif len(players) == 5:
                    self.screen.blit(self.medal3, (170,730))
            # Display top three players
            size = 50
            # Name sizing
            for letter in players[0][1]:
                size -= 2
            self.name_font = self.py.font.SysFont('Arial', size)

            self.screen.blit(self.score_name_panel, (205,550))
            # Score
            self.score_1 = self.score_font.render(players[0][0], True, (0,0,0))
            self.screen.blit(self.score_1, (265,580))
            # Name
            self.name_1 = self.name_font.render(players[0][1], True, (0,0,0))
            self.screen.blit(self.name_1, (430,580))

            self.screen.blit(self.score_name_panel, (205,630))
            size = 50
            for letter in players[1][1]:
                size -= 2
            self.name_font = self.py.font.SysFont('Arial', size)

            self.score_2 = self.score_font.render(players[1][0], True, (0,0,0))
            self.screen.blit(self.score_2, (265,660))
            self.name_2 = self.name_font.render(players[1][1], True, (0,0,0))
            self.screen.blit(self.name_2, (430,660))

            
            self.screen.blit(self.score_name_panel, (205,710))
            size = 50
            for letter in players[2][1]:
                size -= 2
            self.name_font = self.py.font.SysFont('Arial', size)

            self.score_3 = self.score_font.render(players[2][0], True, (0,0,0))
            self.screen.blit(self.score_3, (265,740))
            self.name_3 = self.name_font.render(players[2][1], True, (0,0,0))
            self.screen.blit(self.name_3, (430,740))
        if len(players) > 1:
            self.screen.blit(self.sort_buttons, (60,585))
            self.sort_rect = self.py.Rect(75,600, 70, 70)
            collide_sort_highest = self.sort_rect.collidepoint(self.pos) 
            self.sort_rect2 = self.py.Rect(75,695, 70, 70)
            collide_sort_lowest = self.sort_rect2.collidepoint(self.pos) 
    else:
        self.no_users = self.score_font.render("No registered users have played yet", True, (0,0,0))
        self.screen.blit(self.no_users, (160,640))
    self.screen.blit(self.score_name_text, (210,490))

    self.screen.blit(self.logo, (600,150))
    self.screen.blit(self.start_button, (790,440))
    self.screen.blit(self.options_button, (790,560))
    self.screen.blit(self.account_button, (790,680))
    self.screen.blit(self.exit_button, (830,820))
    
    self.start_rect = self.py.Rect(820,460, 230, 100)
    collide_start = self.start_rect.collidepoint(self.pos)
    self.options_rect = self.py.Rect(820,580, 230, 100) 
    collide_options = self.options_rect.collidepoint(self.pos)
    self.account_rect = self.py.Rect(820,700, 230, 100) 
    collide_account = self.account_rect.collidepoint(self.pos) 
    self.exit_rect = self.py.Rect(855,840, 160, 80) 
    collide_exit = self.exit_rect.collidepoint(self.pos) 

    

    display_account(self, logged_in, user)

    #DEBUG
    # self.py.draw.rect(self.screen, GREY, self.start_rect)
    # self.py.draw.rect(self.screen, RED, self.options_rect)
    # self.py.draw.rect(self.screen, BLUE, self.account_rect)
    # self.py.draw.rect(self.screen, BLUE, self.exit_rect)

def options_screen(self, logged_in, user):
    global collide_input_max_card, collide_input_new_card, collide_input_rect_bg1, collide_input_rect_bg2, collide_input_rect_bg3, collide_input_rect_music, collide_input_rect_sfx, collide_back, collide_save_options
    self.title_font = self.py.font.SysFont('Arial', 50)
    self.screen.fill(WHITE)
    self.bg_plains.set_alpha(150)
    self.screen.blit(self.bg_plains, (0,0))
    self.screen.blit(self.options_panel, (280,60))
    self.max_card_amount_text = self.title_font.render('Max card amount: ', True, (0, 0, 0))
    self.new_cards_each_round_text = self.title_font.render('New cards each round: ', True, (0, 0, 0))
    self.title_text = self.title_font.render('Options', True, (0, 0, 0))
    # Text input system

    # Text input
    self.input_font = self.py.font.SysFont('Arial', 50)
    self.max_card_text_surface = self.input_font.render(self.max_card_count_text, True, (0,0,0))
    self.screen.blit(self.max_card_text_surface, (610, 470))
    self.new_card_text_surface = self.input_font.render(self.new_card_count_text, True, (0,0,0))
    self.screen.blit(self.new_card_text_surface, (610, 710))
    self.music_volume_text_surface = self.input_font.render(self.music_volume_text, True, (0,0,0))
    self.screen.blit(self.music_volume_text_surface, (1095, 577))
    self.sfx_volume_text_surface = self.input_font.render(self.sfx_volume_text, True, (0,0,0))
    self.screen.blit(self.sfx_volume_text_surface, (1098, 730))

    self.input_rect_max_card = self.py.Rect(610, 470, 120, 100) 
    collide_input_max_card = self.input_rect_max_card.collidepoint(self.pos) 
    self.input_rect_new_card = self.py.Rect(610, 710, 120, 100) 
    collide_input_new_card = self.input_rect_new_card.collidepoint(self.pos)
    self.input_rect_bg1 = self.py.Rect(960, 405, 120, 100) 
    collide_input_rect_bg1 = self.input_rect_bg1.collidepoint(self.pos)
    self.input_rect_bg2 = self.py.Rect(1090, 405, 120, 100) 
    collide_input_rect_bg2 = self.input_rect_bg2.collidepoint(self.pos)
    self.input_rect_bg3 = self.py.Rect(1220, 405, 120, 100) 
    collide_input_rect_bg3 = self.input_rect_bg3.collidepoint(self.pos)
    self.input_rect_music = self.py.Rect(1095, 577, 100, 70) 
    collide_input_rect_music = self.input_rect_music.collidepoint(self.pos)
    self.input_rect_sfx = self.py.Rect(1098, 730, 100, 70) 
    collide_input_rect_sfx = self.input_rect_sfx.collidepoint(self.pos)
    self.back_rect = self.py.Rect(1260, 820, 180, 100) 
    collide_back = self.back_rect.collidepoint(self.pos)
    self.save_options_rect = self.py.Rect(400, 820, 180, 100) 
    collide_save_options = self.save_options_rect.collidepoint(self.pos)
    

    # Text boxes
    print("SCREENS: MAX CARD TYPE?", self.typing_max_card_count)
    if self.typing_max_card_count:
        self.py.draw.rect(self.screen, GREY, self.input_rect_max_card, 4)
    elif self.typing_new_card_count:
        self.py.draw.rect(self.screen, GREY, self.input_rect_new_card, 4)
    elif self.typing_music_volume:
        self.py.draw.rect(self.screen, GREY, self.input_rect_music, 4)
    elif self.typing_sfx_volume:
        self.py.draw.rect(self.screen, GREY, self.input_rect_sfx, 4)

    display_account(self, logged_in, user)
    # DEBUG
    # self.py.draw.rect(self.screen, RED, self.back_rect)
    # self.py.draw.rect(self.screen, RED, self.save_options_rect)
    # self.py.draw.rect(self.screen, BLUE, self.input_rect_max_card)
    # self.py.draw.rect(self.screen, GREY, self.input_rect_new_card)
    # self.py.draw.rect(self.screen, RED, self.input_rect_bg1)
    # self.py.draw.rect(self.screen, BLUE, self.input_rect_bg2)
    # self.py.draw.rect(self.screen, GREY, self.input_rect_bg3)
    # self.py.draw.rect(self.screen, GREY, self.input_rect_music)
    # self.py.draw.rect(self.screen, BLUE, self.input_rect_sfx)
def account_choice_screen(self, logged_in, user):
    global collide_login, collide_signin, collide_back
    self.screen.fill(WHITE)
    self.bg_plains.set_alpha(150)
    self.screen.blit(self.bg_plains, (0,0))
    self.screen.blit(self.account_choice_panel, (280,50))
    self.login_rect = self.py.Rect(550, 530, 200, 100) 
    collide_login = self.login_rect.collidepoint(self.pos)
    self.signin_rect = self.py.Rect(1020, 530, 200, 100) 
    collide_signin = self.signin_rect.collidepoint(self.pos)
    self.back_rect = self.py.Rect(1260, 830, 200, 100) 
    collide_back = self.back_rect.collidepoint(self.pos)

    display_account(self, logged_in, user)

    # DEBUG
    # self.py.draw.rect(self.screen, RED, self.back_rect)
    # self.py.draw.rect(self.screen, RED, self.login_rect)
    # self.py.draw.rect(self.screen, RED, self.signin_rect)
def account_login_screen(self, logged_in, user):
    global collide_save_login, collide_back, collide_name_input,collide_password_input
    self.screen.fill(WHITE)
    self.bg_plains.set_alpha(150)
    self.screen.blit(self.bg_plains, (0,0))
    self.screen.blit(self.account_login_panel, (280,50))
    
    # Text input
    self.input_font = self.py.font.SysFont('Arial', 50)
    print("Inputted text:", self.user_name_text)
    self.name_text_surface = self.input_font.render(self.user_name_text, True, (0,0,0))
    self.screen.blit(self.name_text_surface, (755, 540))
    self.password_text_surface = self.input_font.render(self.user_password_text, True, (0,0,0))
    self.screen.blit(self.password_text_surface, (844, 660))

    self.save_login_rect = self.py.Rect(470, 810, 200, 100) 
    collide_save_login = self.save_login_rect.collidepoint(self.pos)
    self.back_rect = self.py.Rect(1260, 810, 200, 100) 
    collide_back = self.back_rect.collidepoint(self.pos)
    self.name_input_rect = self.py.Rect(745, 530, 420, 80) 
    collide_name_input = self.name_input_rect.collidepoint(self.pos)
    self.password_input_rect = self.py.Rect(834, 650, 480, 80) 
    collide_password_input = self.password_input_rect.collidepoint(self.pos)

    if self.typing_name:
        self.py.draw.rect(self.screen, GREY, self.name_input_rect, 4)
    elif self.typing_password:
        self.py.draw.rect(self.screen, GREY, self.password_input_rect, 4)

    display_account(self, logged_in, user)
    # self.py.draw.rect(self.screen, RED, self.save_rect)
    # self.py.draw.rect(self.screen, RED, self.back_rect)
    # self.py.draw.rect(self.screen, RED, self.password_input_rect)
    # self.py.draw.rect(self.screen, RED, self.name_input_rect)
def account_signin_screen(self, logged_in, user):
    global collide_save_account, collide_back, collide_name_input, collide_password_input
    self.screen.fill(WHITE)
    self.bg_plains.set_alpha(150)
    self.screen.blit(self.bg_plains, (0,0))
    self.screen.blit(self.account_signin_panel, (280,50))
    self.save_account_rect = self.py.Rect(470, 810, 200, 100) 
    collide_save_account = self.save_account_rect.collidepoint(self.pos)
    self.back_rect = self.py.Rect(1260, 810, 200, 100) 
    collide_back = self.back_rect.collidepoint(self.pos)

    # Text input
    self.input_font = self.py.font.SysFont('Arial', 50)
    print("Inputted text:", self.user_name_text)
    self.name_text_surface = self.input_font.render(self.user_name_text, True, (0,0,0))
    self.screen.blit(self.name_text_surface, (755, 540))
    self.password_text_surface = self.input_font.render(self.user_password_text, True, (0,0,0))
    self.screen.blit(self.password_text_surface, (844, 660))

    self.name_input_rect = self.py.Rect(745, 530, 420, 80) 
    collide_name_input = self.name_input_rect.collidepoint(self.pos)
    self.password_input_rect = self.py.Rect(834, 650, 480, 80) 
    collide_password_input = self.password_input_rect.collidepoint(self.pos)

    if self.typing_name:
        self.py.draw.rect(self.screen, GREY, self.name_input_rect, 4)
    elif self.typing_password:
        self.py.draw.rect(self.screen, GREY, self.password_input_rect, 4)

    display_account(self, logged_in, user)

    # self.py.draw.rect(self.screen, RED, self.save_account_rect)
    # self.py.draw.rect(self.screen, RED, self.back_rect)
    # self.py.draw.rect(self.screen, RED, self.password_input_rect)
    # self.py.draw.rect(self.screen, RED, self.name_input_rect)
def win_screen(self):
    global collide_back_end
    self.screen.fill(WHITE)
    self.title_text = self.title_font.render('Win!', True, (0, 0, 0))
    self.screen.blit(self.title_text, (750,400))
    self.score_text = self.title_font.render('Score: '+ str(self.current_score), True, (0, 0, 0))
    self.screen.blit(self.score_text, (750,500))
    self.back_end_rect = self.py.Rect(550, 530, 200, 100) 
    collide_back_end = self.back_end_rect.collidepoint(self.pos)
    self.py.draw.rect(self.screen, RED, self.back_end_rect)
def draw_screen(self):
    global collide_back_end
    self.screen.fill(WHITE)
    self.title_text = self.title_font.render('Draw...', True, (0, 0, 0))
    self.screen.blit(self.title_text, (750,400))
    self.score_text = self.title_font.render('Score: '+ str(self.current_score), True, (0, 0, 0))
    self.screen.blit(self.score_text, (750,500))
    self.back_end_rect = self.py.Rect(550, 530, 200, 100) 
    collide_back_end = self.back_end_rect.collidepoint(self.pos)
    self.py.draw.rect(self.screen, RED, self.back_end_rect)
def loss_screen(self):
    global collide_back_end
    self.screen.fill(WHITE)
    self.title_text = self.title_font.render('Loss!', True, (0, 0, 0))
    self.screen.blit(self.title_text, (750,400))
    self.score_text = self.title_font.render('Score: '+ str(self.current_score), True, (0, 0, 0))
    self.screen.blit(self.score_text, (750,500))
    self.back_end_rect = self.py.Rect(550, 530, 200, 100) 
    collide_back_end = self.back_end_rect.collidepoint(self.pos)
    self.py.draw.rect(self.screen, RED, self.back_end_rect)
def back(self):
    global collide_back, collide_login, collide_signin
    collide_back = False
    collide_login = False
    collide_signin = False
    self.typing_name = False
    self.typing_password = False
    self.typing_max_card_count = False
    self.typing_new_card_count = False
    self.typing_music_volume = False
    self.typing_sfx_volume = False
def screen_management(self):
    if self.start_screen_active:
        # If not playing background music, then play
        if self.py.mixer.music.get_busy() is False or self.music_playing is not "menu":
            self.py.mixer.music.load('Sounds/menu.mp3')
            self.py.mixer.music.play(-1)
            self.py.mixer.music.set_volume(float(self.music_volume_text)/100)
            for sound_effect in self.sfx_list:
                sound_effect.set_volume(float(self.sfx_volume_text)/100)
            self.music_playing = "menu"
        start_screen(self, self.logged_in, self.user)
    if self.options_open:
        options_screen(self, self.logged_in, self.user)
    if self.account_choice_open:
        account_choice_screen(self, self.logged_in, self.user)
    if self.account_login_open:
        account_login_screen(self, self.logged_in, self.user)
    if self.account_signin_open:
        account_signin_screen(self, self.logged_in, self.user)
    # PLAY
    if self.play_screen_active:
        print("Play")
        if self.py.mixer.music.get_busy() is False or self.music_playing is not "play1":
            self.py.mixer.music.load('Sounds/play1.mp3')
            self.py.mixer.music.play(-1)
            self.py.mixer.music.set_volume(float(self.music_volume_text)/100)
            self.music_playing = "play1"
        if self.bg_choice == "plains":
            self.screen.blit(plains, (0,0))
        elif self.bg_choice == "desert":
            self.screen.blit(desert, (0,0))
        elif self.bg_choice == "jungle":
            self.screen.blit(jungle, (0,0))
        # End turn button
        self.title_font = self.py.font.SysFont('Arial', 40)
        self.score_text = self.title_font.render('Score: '+ str(self.current_score), True, (255, 255, 255))
        self.screen.blit(self.score_text, (20,20))
        
        self.screen.blit(self.end_turn_button, (25,850))
        self.end_turn_button_rect = self.py.Rect(150, 800, 200, 150) # end turn collsion rect
        self.collide_end_turn_button = self.end_turn_button_rect.collidepoint(self.pos) # check if cursor is over rect (end turn button)
        # First round
        if self.round_count == 1 and self.generated_cards == False: # First round and cards have not yet beet generated
            # PS: self represents instance of the class self
            card.generate_cards(self, self.max_card_amount) # Generate deck of card for both player and pc
            self.loading = False # Turn off loading screen
        # Not first round
        elif self.round_count > 1 and self.added_new_cards == False: # Checks if not first turn and havent already added new cards to each deck
            card.generate_cards(self, 1) # Generate deck of card for both player and pc
            self.loading = False
            self.added_new_cards = True
        # elif self.round_count > 1 and self.added_new_cards == True and self.sorting_cards == False and self.turn is not "PC":
        #     if self.sorted_at_turn_start is False:
        #         print("Sorting as turn start")
        #         self.sorted_at_turn_start = True
        #         self.sort_cards(self) # sort cards before turn start for safety (in case a new card is added)
    
def handle_selection(self):
    global collide_save_options, collide_account
    if self.start_screen_active: 
        # START SCREEEN
        # print("START")
        # Start button collision
        if collide_start:
            print("Colliding with START")
            self.click_sound.play()
            self.loading = True
            # Switch to play screen
            self.start_screen_active = False
            self.play_screen_active = True
        if collide_sort_highest:
            self.click_sound.play()
            self.sort_by_high = True
        if collide_sort_lowest:
            self.click_sound.play()
            self.sort_by_high = False
        # Open options menu
        if collide_options:
            print("OPTIONS")
            self.click_sound.play()
            self.account_choice_open = False
            self.options_open = True
            # Return back to previous screen
        if self.options_open:
            if collide_back:
                self.switch_sound.play()

                self.account_choice_open = False
                self.options_open = False
                self.start_screen_active = True

                back(self)
                print("BACK")
            if collide_save_options:
                print("CHANGE OPTIONS")
                self.new_round_sound.play()
                file_manager.File_Manager.change_options(self, self.user_name_text, self.user_password_text, self.max_card_count_text, self.new_card_count_text, self.bg_choice, self.music_volume_text, self.sfx_volume_text)
                collide_save_options = False
                if self.user_name_text != "":
                    self.options_changed = True
                self.py.mixer.music.set_volume(float(self.music_volume_text)/100)
                for sound_effect in self.sfx_list:
                    sound_effect.set_volume(float(self.sfx_volume_text)/100)
                # SAVED text show
                self.saved_font = self.py.font.SysFont('Arial', 50, True, True)
                self.saved_surface = self.saved_font.render("SAVED", True, (150,255,150), GREY)
                self.screen.blit(self.saved_surface, (600, 840))
                self.py.display.update()
                self.py.time.delay(500)
            if collide_input_max_card:
                self.toggle_sound.play()
                self.typing_name = False
                self.typing_password = False
                self.typing_new_card_count = False
                self.typing_music_volume = False
                self.typing_sfx_volume = False
                self.typing_max_card_count = True
                
            if collide_input_new_card:
                self.toggle_sound.play()
                self.typing_name = False
                self.typing_password = False
                self.typing_max_card_count = False
                self.typing_music_volume = False
                self.typing_sfx_volume = False
                self.typing_new_card_count = True
            if collide_input_rect_music:
                self.toggle_sound.play()
                self.typing_name = False
                self.typing_password = False
                self.typing_max_card_count = False
                self.typing_new_card_count = False
                self.typing_sfx_volume = False
                self.typing_music_volume = True
            if collide_input_rect_sfx:
                self.toggle_sound.play()
                self.typing_name = False
                self.typing_password = False
                self.typing_max_card_count = False
                self.typing_new_card_count = False
                self.typing_music_volume = False
                self.typing_sfx_volume = True
            if collide_input_rect_bg1:
                self.toggle_sound.play()
                self.bg_choice = 'plains'
            if collide_input_rect_bg2:
                self.toggle_sound.play()
                self.bg_choice = 'desert'
            if collide_input_rect_bg3:
                self.toggle_sound.play()
                self.bg_choice = 'jungle'
        # Open account menu
        if collide_account:
            print("ACCOUNT")
            self.click_sound.play()
            self.options_open = False
            self.account_choice_open = True
            self.account_choice_open = True
            # Return back to previous screen
        if collide_back and self.account_choice_open:
            self.switch_sound.play()
            self.options_open = False
            self.account_choice_open = False
            self.start_screen_active = True
            back(self)
            print("BACK")
            
        # Sign in
        if collide_signin:
            self.click_sound.play()
            self.account_choice_open = False
            collide_account = False
            self.account_signin_open = True
            self.account_login_open = False
            account_signin_screen(self, self.logged_in, self.user)
        if self.account_signin_open:
            if collide_name_input:
                self.toggle_sound.play()
                self.typing_password = False
                self.typing_max_card_count = False
                self.typing_new_card_count = False
                self.typing_music_volume = False
                self.typing_sfx_volume = False
                self.typing_name = True
            if collide_password_input:
                self.toggle_sound.play()
                self.typing_name = False
                self.typing_max_card_count = False
                self.typing_new_card_count = False
                self.typing_music_volume = False
                self.typing_sfx_volume = False
                self.typing_password = True
            # Return back to previous screen
            if collide_back:
                self.switch_sound.play()
                self.start_screen_active = True
                self.account_signin_open = False
                back(self)
                print("BACK")
            # Pressing save button
            if collide_save_account:
                print("SAVE")
                self.new_round_sound.play()
                result = file_manager.File_Manager.add_account(self, self.user_name_text, self.user_password_text)
                if result == "ACCOUNT ADDED":
                    self.saved_font = self.py.font.SysFont('Arial', 40, True, True)
                    self.saved_surface = self.saved_font.render("ADDED ACCOUNT", True, (150,255,150), GREY)
                    self.screen.blit(self.saved_surface, (660, 830))
                    self.py.display.update()
                    self.py.time.delay(500)
                    self.logged_in = True
                    self.user = self.user_name_text
                elif result == "ACCOUNT ALREADY EXISTS":
                    self.saved_font = self.py.font.SysFont('Arial', 30, True, True)
                    self.saved_surface = self.saved_font.render("ACCOUNT ALREADY EXISTS", True, (150,255,150), GREY)
                    self.screen.blit(self.saved_surface, (660, 840))
                    self.py.display.update()
                    self.py.time.delay(500)
                elif result == "EMPTY TEXT":
                    self.saved_font = self.py.font.SysFont('Arial', 30, True, True)
                    self.saved_surface = self.saved_font.render("EMPTY", True, (150,255,150), GREY)
                    self.screen.blit(self.saved_surface, (660, 840))
                    self.py.display.update()
                    self.py.time.delay(500)
        # Log in
        if collide_login:
            print("LOGIN 1st")
            self.click_sound.play()
            self.account_choice_open = False
            collide_account = False
            self.account_login_open = True
            self.account_signin_open = False
            account_login_screen(self, self.logged_in, self.user)
            # Return back to previous screen
        if self.account_login_open:
            if collide_back:
                self.switch_sound.play()
                self.start_screen_active = True
                self.account_login_open = False
                back(self)
                print("BACK T")
            # Pressing name input text box
            elif collide_name_input:
                self.toggle_sound.play()
                self.typing_name = True
                self.typing_password = False
            # Pressing password input text box
            elif collide_password_input:
                self.toggle_sound.play()
                self.typing_password = True
                self.typing_name = False
            # Pressing login button
            elif collide_save_login:
                print("FILE LOGIN")
                self.new_round_sound.play()
                result = file_manager.File_Manager.login(self, self.user_name_text, self.user_password_text)
                if result == "LOGGED IN":
                    self.saved_font = self.py.font.SysFont('Arial', 40, True, True)
                    self.saved_surface = self.saved_font.render("LOGGED IN", True, (150,255,150), GREY)
                    self.screen.blit(self.saved_surface, (660, 830))
                    self.py.display.update()
                    self.py.time.delay(500)
                    self.logged_in = True
                    self.user = self.user_name_text
                elif result == "NO ACCOUNT FOUND":
                    self.saved_font = self.py.font.SysFont('Arial', 30, True, True)
                    self.saved_surface = self.saved_font.render("NO ACCOUNT FOUND", True, (150,255,150), GREY)
                    self.screen.blit(self.saved_surface, (660, 830))
                    self.py.display.update()
                    self.py.time.delay(500)
                
        # Exit self
        if collide_exit:
            self.click_sound.play()
            self.py.time.delay(100) # delay exiting so that sound plays
            print("EXIT self")
            self.py.quit()
            sys.exit()

    # Cards have already been generated and collisiosn have been checked earlier
    if self.generated_cards and self.collisions_checked:
        print("One")
        # Cursor colliding with end turn button and clicking (Player wants to end their turn)
        if self.collide_end_turn_button:
            print("Colliding with end turn button")
            round_manager.end_turn(self)
        game_logic.handle_card_selection(self)
def reset_game(self):
    global collide_back, collide_login, collide_signin
    print("Resetting")
    # Only add score to leaderboard if won the self
    if self.won:
        file_manager.File_Manager.add_account_with_score(self, self.user, self.user_password_text, self.current_score)
    self.start_screen_active = True
    self.play_screen_active = False
    self.won = False
    self.lost = False
    self.generated_cards = False
    self.battling = False
    self.sorting_cards = False
    self.selected_card = None
    self.card_selected = False
    self.card_selected_rect = None
    self.card_to_collide = False
    self.pc_battled_all_cards_count = 0
    self.player_battled_all_cards_count = 0
    self.round_count = 1
    self.turn_count = 1
    self.turn = "PLAYER"
    self.next_turn = "PC"
    self.player_cards.clear()
    self.pc_cards.clear()
    self.current_score = 0
    self.added_new_cards = False
    self.display_turn is False
    collide_back = False
    collide_login = False
    collide_signin = False
    self.typing_name = False
    self.typing_password = False
    self.typing_max_card_count = False
    self.typing_new_card_count = False
    self.typing_music_volume = False
    self.typing_sfx_volume = False
    self.sorted_at_turn_start = False
    self.objects_to_display.clear()