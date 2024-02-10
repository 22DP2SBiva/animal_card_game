import sys
import pygame

# Constants
WIDTH, HEIGHT = 1920, 1080
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Circle of !Fight")

        self.clock = pygame.time.Clock()

        # Flags to track current state
        self.start_screen_active = True
        self.play_screen_active = False
        self.win_screen_active = False
        self.lose_screen_active = False
        
    def run(self):
        while True:
            self.screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_UP:
                #         self.movement[0] = True
                #     if event.key == pygame.K_DOWN:
                #         self.movement[1] = True
                # if event.type == pygame.KEYUP:
                #     if event.key == pygame.K_UP:
                #         self.movement[0] = False
                #     if event.key == pygame.K_DOWN:
                #         self.movement[1] = False
            
            pygame.display.update()
            self.clock.tick(60)

Game().run()
