import sys
import pygame
from random import randint
import pygame.color
from Tools.demo.spreadsheet import center

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

# Images
birdImg = pygame.transform.scale(pygame.image.load("imgs/bird.png"), (37, 27))
birdImgRotated = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("imgs/bird.png"), (37, 27)), 30)
birdImgDisRotated = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("imgs/bird.png"), (37, 27)), -30)
columnImg = pygame.transform.scale(pygame.image.load("imgs/column.png"), (450, 1600))
backgroundImg = pygame.transform.scale(pygame.image.load("imgs/background.png"), (1280, 960))
backgroundImgRect = backgroundImg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Game initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLUE)
pygame.display.set_caption("AIGames")
clock = pygame.time.Clock()
running = True
score = 0
fontBase = pygame.font.Font(None, 25)
fontScore = pygame.font.Font(None, 50)
text1 = fontScore.render(str(score), True, (0, 0, 0))


# Classes
class Column:
    def __init__(self):
        self.x = 0
        self.y1 = randint(100, 600)
        self.y2 = HEIGHT - 200 - self.y1
        self.rect = 0
        self.rect1 = columnImg.get_rect(center=(WIDTH - self.x - 205, self.y1 + 30))

    def update(self):
        self.rect1.x = WIDTH - self.x - 205


class Bird:
    def __init__(self, lil, puts):
        self.x = 100
        self.y = HEIGHT // 2
        self.r = 25
        self.lil = lil.copy()
        self.puts = puts.copy()
        self.rect = birdImg.get_rect(center=(self.x - 5, self.y - 30))
        self.jumpTime = 0
        self.score = 0

    def update(self):
        self.rect.y = self.y - 30

    def choose(self):
        rer = 0
        if self.lil[0] > 480 - self.y:
            rer += self.puts[0]
        if self.lil[1] > self.y:
            rer -= self.puts[1]
        if self.lil[2] > HEIGHT - column.y2 - self.y:
            rer += self.puts[2]
        if self.lil[3] > self.y - (HEIGHT - column.y2 - 200):
            rer -= self.puts[3]
        if rer > 0:
            self.jumpTime = 20


# Funcs
def mutation(child):
    r = 4
    child1 = Bird(child.lil.copy(), child.puts.copy())
    for _ in range(r):
        t = randint(0, 3)
        child1.lil[t] += randint(-40, 40)
    randRatio = [-1, 1]
    r = 4
    for _ in range(r):
        t = randint(0, 3)
        child1.puts[t] = randRatio[randint(0, 1)]

    return child1


def generate(group_pop):
    randRatio = [-1, 1]
    for _ in range(group_pop):
        o = Bird([randint(0, 300), randint(0, 300), randint(0, 300), randint(0, 300)],
                 [randRatio[randint(0, 1)], randRatio[randint(0, 1)], randRatio[randint(0, 1)], randRatio[randint(0, 1)]])
        liveBirds.append(o)


# Models
column = Column()
liveBirds = []
deadBirds = []
birdsCount = 40
generation = 0
text2 = fontBase.render(str(generation), True, (0, 0, 0))
generate(birdsCount)

# Game cycle
while running:
    generation += 1
    text2 = fontBase.render("Generation: " + str(generation), True, (0, 0, 0))
    deadBirds = []
    column = Column()
    while len(liveBirds) > 0:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(backgroundImg, backgroundImgRect)
        column.update()
        screen.blit(columnImg, column.rect1)
        if column.x >= WIDTH + 50:
            column = Column()
            score += 1
            text1 = fontScore.render(str(score), True, (0, 0, 0))
        column.x += FPS // 20

        # Columns
        for bird in liveBirds:
            if (WIDTH - column.x <= bird.x + bird.r <= WIDTH - column.x + 50 or
                WIDTH - column.x <= bird.x - bird.r <= WIDTH - column.x + 50) and \
                    not (column.y1 <= bird.y + bird.r <= HEIGHT - column.y2 and
                         column.y1 <= bird.y - bird.r <= HEIGHT - column.y2):
                print("END: COLUMN")
                print(len(liveBirds))
                bird.score = score
                liveBirds.remove(bird)
                deadBirds.append(bird)

            # Bird
            bird.choose()
            if bird.jumpTime > 0:
                if (bird.y - bird.r) - FPS // 4 > 0:
                    bird.y -= bird.jumpTime ** 2 / 15
                bird.jumpTime -= 1
            bird.update()
            if bird.jumpTime > 0:
                screen.blit(birdImgRotated, bird.rect)
            else:
                screen.blit(birdImgDisRotated, bird.rect)
            bird.y += 6
            if bird.y + bird.r >= HEIGHT:
                print("END: FLOOR")
                print(len(liveBirds))
                bird.score = score
                liveBirds.remove(bird)
                deadBirds.append(bird)
        screen.blit(text1, (WIDTH // 2 - 20, 20))
        screen.blit(text2, (0, 20))
        pygame.display.flip()
    score = 0
    text1 = fontScore.render(str(score), True, (0, 0, 0))

    # Score
    parent1 = Bird([randint(10, 470), randint(0, 300), randint(0, 300), randint(0, 300)],
                   [randint(10, 470), randint(0, 300), randint(0, 300), randint(0, 300)])
    parent1.score = -1

    for bird in deadBirds:
        if bird.score > parent1.score:
            parent1 = Bird(bird.lil.copy(), bird.puts.copy())
    if parent1.score == 0:
        generate(birdsCount)
        continue
    liveBirds.append(parent1)
    for i in range(birdsCount - 1):
        liveBirds.append(mutation(parent1))
