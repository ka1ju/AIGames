import sys
import pygame
import pygame.color
import random
from random import randint

# Game parameters
WIDTH = 500
HEIGHT = 1000
FPS = 60
blockWidth = WIDTH // 10
blockHeight = HEIGHT // 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
LIGHT_GREY = (200, 200, 200)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
running = True
score = 0
fontLittle = pygame.font.Font(None, 25)
fontBig = pygame.font.Font(None, 50)
text1 = fontBig.render(str(score), True, (0, 0, 0))
figureTypes = [
    [[1, 1, 0], [0, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]]
]
gameField = []
for _ in range(20):
    gameField.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


# Class
class Figure:
    def __init__(self):
        self.x = randint(0, 7)
        self.y = 0
        self.form = random.choice(figureTypes)
        self.color = random.choice([RED, YELLOW, GREEN, CYAN, BLUE, PURPLE])


for i in range(9):
    pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                     ((i + 1) * blockWidth, 0), ((i + 1) * blockWidth, HEIGHT))
for i in range(19):
    pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                     (0, (i + 1) * blockHeight), (WIDTH, (i + 1) * blockHeight))

movingFigure = Figure()
timer = FPS // 2
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    for i in range(9):
        pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                         ((i + 1) * blockWidth, 0), ((i + 1) * blockWidth, HEIGHT))
    for i in range(19):
        pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                         (0, (i + 1) * blockHeight), (WIDTH, (i + 1) * blockHeight))

    isStop = False
    t = 0
    for j in range(len(movingFigure.form)):
        for i in range(len(movingFigure.form[j])):
            if movingFigure.form[j][i] == 1:
                pygame.draw.rect(screen, movingFigure.color,
                                 ((movingFigure.x + i) * blockWidth, (movingFigure.y + j) * blockHeight,
                                  blockWidth, blockHeight))
            if movingFigure.y + j + 1 == 20 or (gameField[movingFigure.y + j + 1][movingFigure.x + i] == 1 and movingFigure.form[j][i] == 1):
                if movingFigure.y == 0:
                    gameField = []
                    movingFigure = Figure()
                    for _ in range(20):
                        gameField.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                else:
                    isStop = True
    if isStop:
        for j in range(len(movingFigure.form)):
            for i in range(len(movingFigure.form[j])):
                if movingFigure.form[j][i] == 1:
                    gameField[movingFigure.y + j][movingFigure.x + i] = 1
        if [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] in gameField:
            gameField.remove([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            gameField.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            score += 10
        movingFigure = Figure()
    if timer == 0:
        movingFigure.y += 1
        timer = FPS // 2
    else:
        timer -= 1
    for j in range(20):
        for i in range(10):
            if gameField[j][i] == 1:
                pygame.draw.rect(screen, LIGHT_GREY, (i * blockWidth, j * blockHeight, blockWidth, blockHeight))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                if movingFigure.y + len(movingFigure.form) + 1 == 20 or \
                        gameField[movingFigure.y + len(movingFigure.form)] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    movingFigure.y += 1
            if event.key == pygame.K_a:
                if movingFigure.x * WIDTH // 10 >= WIDTH // 10:
                    movingFigure.x -= 1
            if event.key == pygame.K_d:
                if (movingFigure.x + len(
                        max(movingFigure.form, key=lambda x: len(x)))) * WIDTH // 10 <= WIDTH - WIDTH // 10:
                    movingFigure.x += 1
            if event.key == pygame.K_q:
                newFigure = []
                for j in range(len(movingFigure.form[0])):
                    newFigure.append([])
                    for i in range(len(movingFigure.form)):
                        newFigure[j].append(movingFigure.form[i][j])
                movingFigure.form = list(reversed(newFigure))
            if event.key == pygame.K_e:
                newFigure = []
                for j in range(len(movingFigure.form[0])):
                    part = []
                    for i in range(len(movingFigure.form)):
                        part.append(movingFigure.form[i][j])
                    newFigure.append(list(reversed(part)))
                movingFigure.form = newFigure
    text1 = fontBig.render(str(score), True, WHITE)
    screen.blit(text1, (WIDTH // 2 - 7.5, 0))
    pygame.display.flip()
