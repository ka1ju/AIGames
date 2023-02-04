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
        self.timer = FPS // 2
        self.isStop = False


for i in range(9):
    pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                     ((i + 1) * blockWidth, 0), ((i + 1) * blockWidth, HEIGHT))
for i in range(19):
    pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                     (0, (i + 1) * blockHeight), (WIDTH, (i + 1) * blockHeight))

mF = Figure()
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    for i in range(9):
        pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                         ((i + 1) * blockWidth, 0), ((i + 1) * blockWidth, HEIGHT))
    for i in range(19):
        pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                         (0, (i + 1) * blockHeight), (WIDTH, (i + 1) * blockHeight))

    for j in range(len(mF.form)):
        for i in range(len(mF.form[j])):
            if mF.form[j][i] == 1:
                pygame.draw.rect(screen, mF.color,
                                 ((mF.x + i) * blockWidth, (mF.y + j) * blockHeight,
                                  blockWidth, blockHeight))
            if mF.y + j + 1 == 20 or (gameField[mF.y + j + 1][mF.x + i] == 1 and mF.form[j][i] == 1):
                if mF.y == 0:
                    gameField = []
                    mF = Figure()
                    for _ in range(20):
                        gameField.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                    score = 0
                else:
                    mF.isStop = True
    if mF.isStop:
        for j in range(len(mF.form)):
            for i in range(len(mF.form[j])):
                if mF.form[j][i] == 1:
                    gameField[mF.y + j][mF.x + i] = 1
        if [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] in gameField:
            gameField.remove([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            gameField.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            score += 10
        mF = Figure()
    if mF.timer == 0:
        mF.y += 1
        mF.timer = FPS // 2
    else:
        mF.timer -= 1
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
                if mF.y + len(mF.form) + 1 == 20 or \
                        gameField[mF.y + len(mF.form)] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    mF.y += 1
            if event.key == pygame.K_a:
                if mF.x * WIDTH // 10 >= WIDTH // 10:
                    mF.x -= 1
            if event.key == pygame.K_d:
                if (mF.x + len(
                        max(mF.form, key=lambda x: len(x)))) * WIDTH // 10 <= WIDTH - WIDTH // 10:
                    mF.x += 1
            if event.key == pygame.K_q:
                newFigure = []
                for j in range(len(mF.form[0])):
                    newFigure.append([])
                    for i in range(len(mF.form)):
                        newFigure[j].append(mF.form[i][j])
                mF.form = list(reversed(newFigure))
            if event.key == pygame.K_e:
                newFigure = []
                for j in range(len(mF.form[0])):
                    part = []
                    for i in range(len(mF.form)):
                        part.append(mF.form[i][j])
                    newFigure.append(list(reversed(part)))
                mF.form = newFigure
    text1 = fontBig.render(str(score), True, WHITE)
    screen.blit(text1, (WIDTH // 2 - 7.5, 0))
    pygame.display.flip()
