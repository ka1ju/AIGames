import sys
import pygame
import pygame.color
import random
from random import randint
from ai_functions import *
import time
import copy
import json

# Game parameters
distance = 20
game_counts = 20
WIDTH = 500 * game_counts + distance * game_counts
HEIGHT = 1000
FPS = 60
blockWidth = 50
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
    [[1, 0, 0], [1, 1, 1]],
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]]]


# Class
class Figure:
    def __init__(self, dist, ratios):
        self.chosen = False
        self.placed =0
        self.dist = dist
        self.ratio = ratios.copy()
        self.x = randint(0, 6)
        self.y = 0
        self.form = random.choice(figureTypes)
        self.color = random.choice([RED, YELLOW, GREEN, CYAN, BLUE, PURPLE])
        self.timer = 0
        self.isStop = False
        self.gameField = []
        self.score = 0
        for _ in range(20):
            self.gameField.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def update(self):
        self.x = randint(0, 6)
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

games = []
for i in range(game_counts):
    games.append(Figure(500 * i + distance * i, [randint(-50, 50), randint(-50, 50), randint(-50, 50), randint(-50, 50)]))
text1 = fontBig.render(str(0), True, (0, 0, 0))
while running:
    dead_games = []
    print('new games')
    while games:
        clock.tick(FPS)
        text1 = fontBig.render(str(0), True, (0, 0, 0))
        pygame.display.flip()
        screen.fill(BLACK)
        for mf in games:
            if mf.score % 100 == 0 and mf.score > 99:
                best_ratios = mf.ratio.copy()
                best_placed = mf.placed
                best_score = mf.score
                q = {'best_ratios': best_ratios,
                     'best_placed': best_placed,
                     'best_score': best_score}
                f = open('best_statics.json', 'w')
                json.dump(q, f)
                f.close()
            for i in range(9):
                pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                                 ((i + 1) * blockWidth + mf.dist, 0), ((i + 1) * blockWidth + mf.dist, HEIGHT))
            for i in range(19):
                pygame.draw.line(screen, pygame.color.Color(100, 100, 100),
                                 (mf.dist, (i + 1) * blockHeight), (500 + mf.dist, (i + 1) * blockHeight))
            ded = 0
            z = 0
            for j in range(len(mf.form)):
                if z == 0:
                    for i in range(len(mf.form[j])):
                        if z == 0:
                            if mf.form[j][i] == 1:
                                pygame.draw.rect(screen, mf.color,
                                                 ((mf.x + i) * blockWidth + mf.dist, (mf.y + j) * blockHeight,
                                                  blockWidth, blockHeight))
                                if mf.y + j + 1 == 20 or (mf.gameField[mf.y + j + 1][mf.x + i] == 1 and mf.form[j][i] == 1):
                                    z = 1
                                    if mf.y == 0:
                                        games.remove(mf)
                                        dead_games.append(mf)
                                        ded = 1
                                    else:
                                        mf.isStop = True
            if ded == 1:
                continue
            iop = 0
            scoc = 0
            if mf.isStop:
                mf.chosen = False
                for j in range(len(mf.form)):
                    for i in range(len(mf.form[j])):
                        if mf.form[j][i] == 1 and mf.y + j < 20:
                            mf.gameField[mf.y + j][mf.x + i] = 1
                while [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] in mf.gameField:
                    iop += 1
                    mf.gameField.remove([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
                    mf.gameField.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                    scoc += 10
                mf.score += scoc * iop
                mf.update()
                mf.placed += 1
            if mf.timer == 0 and mf.y + len(mf.form) < 20:
                mf.y += 1
                mf.timer = 0
            else:
                mf.timer -= 1
            for j in range(20):
                for i in range(10):
                    if mf.gameField[j][i] == 1:
                        pygame.draw.rect(screen, LIGHT_GREY, (i * blockWidth + mf.dist, j * blockHeight, blockWidth, blockHeight))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            text1 = fontBig.render(str(mf.score), True, WHITE)
            screen.blit(text1, (mf.dist + 250, 0))
            mf1 = copy.deepcopy(mf)
            if mf.chosen:
                strategy_comb = 'd'
            else:
                strategy_comb = choose_best_position(mf1)
                mf.chosen = True
            if mf.form == [[1, 1], [1, 1]] and strategy_comb[0] == 'r':
                strategy_comb[0] = 'd'
            for strategy in strategy_comb:
                if strategy == 'r':
                    if len(mf.form) + mf.x < 10:
                        newFigure = []
                        for j in range(len(mf.form[0])):
                            newFigure.append([])
                            for i in range(len(mf.form)):
                                newFigure[j].append(mf.form[i][j])
                        mf.form = list(reversed(newFigure))
                elif strategy == 'd':
                    if mf.y + len(mf.form) + 1 < 19:
                        if mf.gameField[mf.y + len(mf.form)][mf.x:mf.x + len(mf.form[0])] == [0] * len(mf.form[0]):
                            mf.y += 1
                elif strategy == 'l':
                    if mf.x > 0:
                        k = True
                        for i in range(len(mf.form)):
                            if mf.form[i][0] + mf.gameField[mf.y + i][mf.x - 1] == 2:
                                k = False
                        if k:
                            mf.x -= 1
                elif strategy == 'i':
                    if mf.x + len(mf.form[0]) < 10:
                        k = True
                        for i in range(len(mf.form)):
                            if mf.form[i][-1] + mf.gameField[mf.y + i][mf.x + len(mf.form[0])] == 2:
                                k = False
                        if k:
                            mf.x += 1
    best_ratios = 0
    best_placed = 0
    best_score = 0
    for i in dead_games:
        if best_ratios == 0:
            best_ratios = i.ratio.copy()
            best_placed = i.placed
            best_score = i.score
        elif best_score < i.score:
            best_ratios = i.ratio.copy()
            best_placed = i.placed
            best_score = i.score
        elif best_placed < i.placed and best_score == i.score:
            best_ratios = i.ratio.copy()
            best_placed = i.placed
            best_score = i.score
    q = {'best_ratios': best_ratios,
         'best_placed': best_placed,
         'best_score': best_score}
    f = open('best_statics.json', 'w')
    json.dump(q, f)
    f.close()
    games.append(Figure(500 * 0 + distance * 0, best_ratios.copy()))
    for i in range(1, game_counts):
        ratio = mutation(best_ratios.copy()).copy()
        games.append(Figure(500 * i + distance * i, ratio))
