import random
import copy


def choose_best_positin(mf_def1):
    mf_def = copy.deepcopy(mf_def1)
    variants = [['r', mf_def], ['rr', mf_def], ['rrr', mf_def], ['', mf_def]]
    best_actions_count = 0
    best_strategy = ''
    best_quality = -100000
    for o in variants:
            f = 'l'
            for u in range(10):
                y = o[0]
                y = y + f * u
                f = 'i'
                mf = copy.deepcopy(mf_def)
                z = 0
                for t in y:
                    if t == 'r':
                        newFigure = []
                        for j in range(len(mf.form[0])):
                            newFigure.append([])
                            for i in range(len(mf.form)):
                                newFigure[j].append(mf.form[i][j])
                        mf.form = list(reversed(newFigure))
                        if len(mf.form[0]) == 3 and mf.x + 2 == 10:
                            mf.x -= 1
                    elif t == 'l':
                        if mf.x > 0:
                            k = True
                            for i in range(len(mf.form)):
                                if mf.form[i][0] + mf.gameField[mf.y + i][mf.x - 1] == 2:
                                    k = False
                            if k:
                                mf.x -= 1
                    elif t == 'i':
                        if mf.x + len(mf.form[0]) < 10:
                            k = True
                            for i in range(len(mf.form)):
                                if mf.form[i][-1] + mf.gameField[mf.y + i][mf.x + len(mf.form[0])] == 2:
                                    k = False
                            if k:
                                mf.x += 1
                while z == 0:
                    for j in range(len(mf.form)):
                        for i in range(len(mf.form[j])):
                            if mf.form[j][i] == 1:
                                if mf.y + j + 1 == 20 or (mf.gameField[mf.y + j + 1][mf.x + i] == 1 and mf.form[j][i] == 1):
                                    z = 1
                                    q = quality(mf)
                                    if y == '':
                                        y = 'd'
                                    if q > best_quality:
                                        best_quality = q
                                        best_strategy = y[0]
                                        best_actions_count = len(y)
                                    elif q == best_quality and best_actions_count > len(y):
                                        best_quality = q
                                        best_strategy = y[0]
                                        best_actions_count = len(y)
                    mf.y += 1


    return best_strategy


def quality(mf_def):
    mf = copy.deepcopy(mf_def)
    score = 0
    holes = 0
    mn = 0
    high = mf.y
    for j in range(len(mf.form)):
        for i in range(len(mf.form[j])):
            if mf.form[j][i] == 1:
                mf.gameField[mf.y + j][mf.x + i] = 1
    while [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] in mf.gameField:
        mf.gameField.remove([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        mf.gameField.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        score += 10
        mn += 1
    score *= mn
    for i in range(1, 20):
        for j in range(10):
            if mf.gameField[i][j] == 0 and mf.gameField[i - 1][j] == 1:
                holes += 1
    return score - holes + high


'''        mf1 = mf
    mf1.form = mf.form.copy()
    mf1.gameField = mf.gameField.copy()
    strategy = choose_best_positin(mf1)
    if strategy == 'r':
        newFigure = []
        for j in range(len(mf.form[0])):
            newFigure.append([])
            for i in range(len(mf.form)):
                newFigure[j].append(mf.form[i][j])
        mf.form = list(reversed(newFigure))
        if len(mf.form[0]) == 3 and mf.x + 2 == 10:
            mf.x -= 1
    elif strategy == 'd':
        if mf.y + len(mf.form) + 1 != 20 or \
                mf.gameField[mf.y + len(mf.form)][mf.x:mf.x + len(mf.form[1])] == [0, 0, 0]:
            mf.y += 1
    elif strategy == 'l':
        if mf.x > 0:
            k = True
            for i in range(len(mf.form)):
                if mf.form[i][0] + mf.gameField[mf.y + i][mf.x - 1] == 2:
                    k = False
            if k:
                mf.x -= 1
    elif strategy == 'ri':
        if mf.x + len(mf.form[0]) < 10:
            k = True
            for i in range(len(mf.form)):
                if mf.form[i][-1] + mf.gameField[mf.y + i][mf.x + len(mf.form[0])] == 2:
                    k = False
            if k:
                mf.x += 1'''


'''        if event.type == pygame.KEYUP:
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
                    mf.x -= 1'''