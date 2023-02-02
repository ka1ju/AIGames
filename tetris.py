import sys
import pygame
import pygame.color
import random
from random import randint

# Game parameters
WIDTH = 400
HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
running = True
score = 0
fontLittle = pygame.font.Font(None, 25)
fontBig = pygame.font.Font(None, 50)
text1 = fontBig.render(str(score), True, (0, 0, 0))


# Class
class Figure:
    def __init__(self):
        self.x = randint(0, 7)
        self.y = 0
        self.form = []


movingFigure = Figure()
figures = []
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                movingFigure.x -= 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                pass
            if event.key == pygame.K_d:
                pass
            if event.key == pygame.K_q:
                pass
            if event.key == pygame.K_e:
                pass
    pygame.display.flip()
