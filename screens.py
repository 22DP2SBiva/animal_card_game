# for storing and displaying screens
# pylint: disable=no-member
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
class Screens:
    def __init__(self, pygame_instance, screen, pos, user_name_text, user_password_text, typing_name, typing_password, typing_max_card_count, typing_new_card_count, typing_music_volume, typing_sfx_volume, max_card_count_text, new_card_count_text, music_volume_text, sfx_volume_text):
        self.py = pygame_instance # Refrence pygame from Game class
        self.screen = screen # Refrence screen from Game class
        self.pos = pos # Refrence pos from game class
        self.user_name_text = user_name_text
        self.user_password_text = user_password_text
        self.typing_name = typing_name
        self.typing_password = typing_password
        self.typing_max_card_count = typing_max_card_count
        self.typing_new_card_count = typing_new_card_count
        self.typing_music_volume = typing_music_volume
        self.typing_sfx_volume = typing_sfx_volume
        self.max_card_count_text = max_card_count_text
        self.new_card_count_text = new_card_count_text
        self.music_volume_text = music_volume_text
        self.sfx_volume_text = sfx_volume_text


        self.collide_login = False
        self.collide_signin = False
        self.collide_back = False
        self.collide_name_input = False
        self.collide_password_input = False
        self.collide_save = False
        self.collide_start = False
        self.collide_options = False
        self.collide_exit = False
        self.collide_account = False
        self.collide_save_options = False
        self.collide_input_max_card = False
        self.collide_input_new_card = False
        self.collide_input_rect_bg1 = False
        self.collide_input_rect_bg2 = False
        self.collide_input_rect_bg3 = False
        self.collide_input_rect_music = False
        self.collide_input_rect_sfx = False
        self.collide_back = False
        self.collide_save_options = False
        self.collide_save_account = False
        self.collide_name_input = False
        self.collide_password_input = False

        self.title_font = self.py.font.SysFont('Arial', 50)
    def start_screen(self):
        # Background
        self.bg_plains = self.py.image.load("Assets/bg_plains.png").convert_alpha()
        self.screen.blit(self.bg_plains, (0,0))
        # IMAGES
        self.start_button = self.py.image.load("Assets/start_button.png").convert_alpha()
        self.options_button = self.py.image.load("Assets/options_button.png").convert_alpha()
        self.account_button = self.py.image.load("Assets/account_button.png").convert_alpha()
        self.exit_button = self.py.image.load("Assets/exit_button.png").convert_alpha()
        self.logo = self.py.image.load("Assets/logo.png").convert_alpha()
        

        self.start_button = self.py.transform.scale(self.start_button, (1200,900))
        self.options_button = self.py.transform.scale(self.options_button, (1200,900))
        self.account_button = self.py.transform.scale(self.account_button, (1200,900))
        self.exit_button = self.py.transform.scale(self.exit_button, (1200,900))

        self.screen.blit(self.logo, (600,150))
        self.screen.blit(self.start_button, (790,440))
        self.screen.blit(self.options_button, (790,560))
        self.screen.blit(self.account_button, (790,680))
        self.screen.blit(self.exit_button, (830,820))
        

        self.start_rect = self.py.Rect(820,460, 230, 100) # start button collsion rect
        self.collide_start = self.start_rect.collidepoint(self.pos) # check if cursor is over rect (start button)
        self.options_rect = self.py.Rect(820,580, 230, 100) # start button collsion rect
        self.collide_options = self.options_rect.collidepoint(self.pos) # check if cursor is over rect (start button)
        self.account_rect = self.py.Rect(820,700, 230, 100) # start button collsion rect
        self.collide_account = self.account_rect.collidepoint(self.pos) # check if cursor is over rect (start button)
        self.exit_rect = self.py.Rect(855,840, 160, 80) # start button collsion rect
        self.collide_exit = self.exit_rect.collidepoint(self.pos) # check if cursor is over rect (start button)

        #DEBUG
        # self.py.draw.rect(self.screen, GREY, self.start_rect)
        # self.py.draw.rect(self.screen, RED, self.options_rect)
        # self.py.draw.rect(self.screen, BLUE, self.account_rect)
        # self.py.draw.rect(self.screen, BLUE, self.exit_rect)

    def options_screen(self):
        self.bg_plains = self.py.image.load("Assets/bg_plains.png").convert_alpha()
        self.screen.blit(self.bg_plains, (0,0))
        self.options_panel = self.py.image.load("Assets/options_panel.png").convert_alpha()
        self.options_panel = self.py.transform.scale(self.options_panel, (1700,1100))
        self.screen.blit(self.options_panel, (280,60))
        self.options_panel = self.py.transform.scale(self.options_panel, (1200,900))
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
        self.collide_input_max_card = self.input_rect_max_card.collidepoint(self.pos) 
        self.input_rect_new_card = self.py.Rect(610, 710, 120, 100) 
        self.collide_input_new_card = self.input_rect_new_card.collidepoint(self.pos)
        self.input_rect_bg1 = self.py.Rect(960, 405, 120, 100) 
        self.collide_input_rect_bg1 = self.input_rect_bg1.collidepoint(self.pos)
        self.input_rect_bg2 = self.py.Rect(1090, 405, 120, 100) 
        self.collide_input_rect_bg2 = self.input_rect_bg2.collidepoint(self.pos)
        self.input_rect_bg3 = self.py.Rect(1220, 405, 120, 100) 
        self.collide_input_rect_bg3 = self.input_rect_bg3.collidepoint(self.pos)
        self.input_rect_music = self.py.Rect(1095, 577, 100, 70) 
        self.collide_input_rect_music = self.input_rect_music.collidepoint(self.pos)
        self.input_rect_sfx = self.py.Rect(1098, 730, 100, 70) 
        self.collide_input_rect_sfx = self.input_rect_sfx.collidepoint(self.pos)
        self.back_rect = self.py.Rect(1260, 820, 180, 100) 
        self.collide_back = self.back_rect.collidepoint(self.pos)
        self.save_options_rect = self.py.Rect(400, 820, 180, 100) 
        self.collide_save_options = self.save_options_rect.collidepoint(self.pos)

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
    def account_choice_screen(self):
        self.bg_plains = self.py.image.load("Assets/bg_plains.png").convert_alpha()
        self.screen.blit(self.bg_plains, (0,0))
        self.account_choice_panel = self.py.image.load("Assets/account_choice_panel.png").convert_alpha()
        self.account_choice_panel = self.py.transform.scale(self.account_choice_panel, (1700,1100))
        self.screen.blit(self.account_choice_panel, (280,50))
        self.login_rect = self.py.Rect(550, 530, 200, 100) 
        self.collide_login = self.login_rect.collidepoint(self.pos)
        self.signin_rect = self.py.Rect(1020, 530, 200, 100) 
        self.collide_signin = self.signin_rect.collidepoint(self.pos)
        self.back_rect = self.py.Rect(1260, 830, 200, 100) 
        self.collide_back = self.back_rect.collidepoint(self.pos)

        # DEBUG
        # self.py.draw.rect(self.screen, RED, self.back_rect)
        # self.py.draw.rect(self.screen, RED, self.login_rect)
        # self.py.draw.rect(self.screen, RED, self.signin_rect)
    def account_login_screen(self):
        self.bg_plains = self.py.image.load("Assets/bg_plains.png").convert_alpha()
        self.screen.blit(self.bg_plains, (0,0))
        self.account_login_panel = self.py.image.load("Assets/login_panel.png").convert_alpha()
        self.account_login_panel = self.py.transform.scale(self.account_login_panel, (1700,1100))
        self.screen.blit(self.account_login_panel, (280,50))
        
        # Text input
        self.input_font = self.py.font.SysFont('Arial', 50)
        print("Inputted text:", self.user_name_text)
        self.name_text_surface = self.input_font.render(self.user_name_text, True, (0,0,0))
        self.screen.blit(self.name_text_surface, (755, 540))
        self.password_text_surface = self.input_font.render(self.user_password_text, True, (0,0,0))
        self.screen.blit(self.password_text_surface, (844, 660))

        self.save_login_rect = self.py.Rect(470, 810, 200, 100) 
        self.collide_save_login = self.save_login_rect.collidepoint(self.pos)
        self.back_rect = self.py.Rect(1260, 810, 200, 100) 
        self.collide_back = self.back_rect.collidepoint(self.pos)
        self.name_input_rect = self.py.Rect(745, 530, 420, 80) 
        self.collide_name_input = self.name_input_rect.collidepoint(self.pos)
        self.password_input_rect = self.py.Rect(834, 650, 480, 80) 
        self.collide_password_input = self.password_input_rect.collidepoint(self.pos)

        if self.typing_name:
            self.py.draw.rect(self.screen, GREY, self.name_input_rect, 4)
        elif self.typing_password:
            self.py.draw.rect(self.screen, GREY, self.password_input_rect, 4)
        # self.py.draw.rect(self.screen, RED, self.save_rect)
        # self.py.draw.rect(self.screen, RED, self.back_rect)
        # self.py.draw.rect(self.screen, RED, self.password_input_rect)
        # self.py.draw.rect(self.screen, RED, self.name_input_rect)
    def account_signin_screen(self):
        self.bg_plains = self.py.image.load("Assets/bg_plains.png").convert_alpha()
        self.screen.blit(self.bg_plains, (0,0))
        self.account_signin_panel = self.py.image.load("Assets/signup_panel.png").convert_alpha()
        self.account_signin_panel = self.py.transform.scale(self.account_signin_panel, (1700,1100))
        self.screen.blit(self.account_signin_panel, (280,50))
        self.save_account_rect = self.py.Rect(470, 810, 200, 100) 
        self.collide_save_account = self.save_account_rect.collidepoint(self.pos)
        self.back_rect = self.py.Rect(1260, 810, 200, 100) 
        self.collide_back = self.back_rect.collidepoint(self.pos)

        # Text input
        self.input_font = self.py.font.SysFont('Arial', 50)
        print("Inputted text:", self.user_name_text)
        self.name_text_surface = self.input_font.render(self.user_name_text, True, (0,0,0))
        self.screen.blit(self.name_text_surface, (755, 540))
        self.password_text_surface = self.input_font.render(self.user_password_text, True, (0,0,0))
        self.screen.blit(self.password_text_surface, (844, 660))

        self.name_input_rect = self.py.Rect(745, 530, 420, 80) 
        self.collide_name_input = self.name_input_rect.collidepoint(self.pos)
        self.password_input_rect = self.py.Rect(834, 650, 480, 80) 
        self.collide_password_input = self.password_input_rect.collidepoint(self.pos)

        if self.typing_name:
            self.py.draw.rect(self.screen, GREY, self.name_input_rect, 4)
        elif self.typing_password:
            self.py.draw.rect(self.screen, GREY, self.password_input_rect, 4)

        # self.py.draw.rect(self.screen, RED, self.save_account_rect)
        # self.py.draw.rect(self.screen, RED, self.back_rect)
        # self.py.draw.rect(self.screen, RED, self.password_input_rect)
        # self.py.draw.rect(self.screen, RED, self.name_input_rect)
    def win_screen(self):
        self.screen.fill(WHITE)
        self.title_text = self.title_font.render('Win!', True, (0, 0, 0))
        self.screen.blit(self.title_text, (750,400))
        # Add PLAY MORE button
    def loss_screen(self):
        self.screen.fill(WHITE)
        self.title_text = self.title_font.render('Loss!', True, (0, 0, 0))
        self.screen.blit(self.title_text, (750,400))
        # Add Try Again button
    def back(self):
        self.collide_back = False
        self.collide_login = False
        self.collide_signin = False
        self.typing_name = False
        self.typing_password = False
        self.typing_max_card_count = False
        self.typing_new_card_count = False
        self.typing_music_volume = False
        self.typing_sfx_volume = False