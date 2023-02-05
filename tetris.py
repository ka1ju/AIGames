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
fontLittle = pygame.font.Font(None, 25)
fontBig = pygame.font.Font(None, 50)
figureTypes = [
    [[1, 1, 0], [0, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]]
]


# Class
class Figure:
    def __init__(self):
        self.x = randint(0, 7)
        self.y = 0
        self.form = random.choice(figureTypes)
        self.color = random.choice([RED, YELLOW, GREEN, CYAN, BLUE, PURPLE])
        self.timer = FPS // 2
        self.isStop = False
        self.gameField = []
        self.score = 0
        for _ in range(20):
            self.gameField.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def update(self):
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

mf = Figure()
text1 = fontBig.render(str(mf.score), True, (0, 0, 0))
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    for i in range(9):
        pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                         ((i + 1) * blockWidth, 0), ((i + 1) * blockWidth, HEIGHT))
    for i in range(19):
        pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                         (0, (i + 1) * blockHeight), (WIDTH, (i + 1) * blockHeight))
    for j in range(len(mf.form)):
        for i in range(len(mf.form[j])):
            if mf.form[j][i] == 1:
                pygame.draw.rect(screen, mf.color,
                                 ((mf.x + i) * blockWidth, (mf.y + j) * blockHeight,
                                  blockWidth, blockHeight))
                if mf.y + j + 1 == 20 or (mf.gameField[mf.y + j + 1][mf.x + i] == 1 and mf.form[j][i] == 1):
                    if mf.y == 0:
                        mf = Figure()
                    else:
                        mf.isStop = True
    if mf.isStop:
        for j in range(len(mf.form)):
            for i in range(len(mf.form[j])):
                if mf.form[j][i] == 1:
                    mf.gameField[mf.y + j][mf.x + i] = 1
        if [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] in mf.gameField:
            mf.gameField.remove([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            mf.gameField.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            mf.score += 10
        mf.update()
    if mf.timer == 0:
        mf.y += 1
        mf.timer = FPS // 2
    else:
        mf.timer -= 1
    for j in range(20):
        for i in range(10):
            if mf.gameField[j][i] == 1:
                pygame.draw.rect(screen, LIGHT_GREY, (i * blockWidth, j * blockHeight, blockWidth, blockHeight))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                if mf.y + len(mf.form) + 1 != 20 or \
                        mf.gameField[mf.y + len(mf.form)][mf.x:mf.x + len(mf.form[1])] == [0, 0, 0]:
                    mf.y += 1
            if event.key == pygame.K_a:
                if mf.x > 0:
                    k = True
                    for i in range(len(mf.form)):
                        if mf.form[i][0] + mf.gameField[mf.y + i][mf.x - 1] == 2:
                            k = False
                    if k:
                        mf.x -= 1
            if event.key == pygame.K_d:
                if mf.x + len(mf.form[0]) < 10:
                    k = True
                    for i in range(len(mf.form)):
                        if mf.form[i][-1] + mf.gameField[mf.y + i][mf.x + len(mf.form[0])] == 2:
                            k = False
                    if k:
                        mf.x += 1
            if event.key == pygame.K_q:
                newFigure = []
                for j in range(len(mf.form[0])):
                    newFigure.append([])
                    for i in range(len(mf.form)):
                        newFigure[j].append(mf.form[i][j])
                mf.form = list(reversed(newFigure))
                if len(mf.form[0]) == 3 and mf.x + 2 == 10:
                    mf.x -= 1
            if event.key == pygame.K_e:
                newFigure = []
                for j in range(len(mf.form[0])):
                    part = []
                    for i in range(len(mf.form)):
                        part.append(mf.form[i][j])
                    newFigure.append(list(reversed(part)))
                mf.form = newFigure
                if len(mf.form[0]) == 3 and mf.x + 2 == 10:
                    mf.x -= 1
    text1 = fontBig.render(str(mf.score), True, WHITE)
    screen.blit(text1, (WIDTH // 2 - 7.5, 0))
    pygame.display.flip()
