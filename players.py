import random
import time
import pygame
import math
from copy import deepcopy
import os, sys


class connect4Player(object):
    def __init__(self, position, seed=0):
        self.position = position
        self.opponent = None
        self.seed = seed
        random.seed(seed)

    def play(self, env, move):
        move = [-1]


class human(connect4Player):

    def play(self, env, move):
        move[:] = [int(input('Select next move: '))]
        while True:
            if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
                break
            move[:] = [int(input('Index invalid. Select next move: '))]


class human2(connect4Player):

    def play(self, env, move):
        done = False
        while (not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.position == 1:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    move[:] = [col]
                    done = True


class randomAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        move[:] = [random.choice(indices)]


class stupidAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        if 3 in indices:
            move[:] = [3]
        elif 2 in indices:
            move[:] = [2]
        elif 1 in indices:
            move[:] = [1]
        elif 5 in indices:
            move[:] = [5]
        elif 6 in indices:
            move[:] = [6]
        else:
            move[:] = [0]


class minimaxAI(connect4Player):

    def play(self, env, move):
        if len(env.history[0]) == 0 and len(env.history[1]) == 0:
            move[:] = [3]
            print("first move finished")
            return
        self.minimax(deepcopy(env), move, 4)
        print("Finished!")

    def simulateMove(self, env, move, player):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)
        return env

    def MAX(self, env, depth):
        if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape[1]:
            return 0
        if env.gameOver(env.history[0][-1], self.opponent.position):
            return -100000
        if depth == 0:
            if self.position == 1:
                return self.eval_p1(env)
            else:
                return self.eval(env)
        max_value = -math.inf
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        for move in indices:
            child = self.simulateMove(deepcopy(env), move, self.position)
            max_value = max(max_value, self.MIN(child, depth - 1))
        return max_value

    def MIN(self, env, depth):
        if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape[1]:
            return 0
        if env.gameOver(env.history[0][-1], self.position):
            return 100000
        if depth == 0:
            if self.position == 1:
                return self.eval_p1(env)
            else:
                return self.eval(env)
        min_value = math.inf
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        for move in indices:
            child = self.simulateMove(deepcopy(env), move, self.opponent.position)
            min_value = min(min_value, self.MAX(child, depth - 1))
        return min_value

    def eval(self, env):
        # ROW_COUNT = 6  # height
        # COLUMN_COUNT = 7  # width
        heur = 0
        state = deepcopy(env)
        for i in range(0, COLUMN_COUNT):
            for j in range(0, ROW_COUNT):
                try:
                    # add player one streak scores to heur
                    if state.board[i][j] == state.board[i + 1][j] == 2:
                        heur += 10
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 2:
                        heur += 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 2:
                        heur += 10000

                    # subtract player two streak score to heur
                    if state.board[i][j] == state.board[i + 1][j] == 1:
                        heur -= 10
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 1:
                        heur -= 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add player one vertical streaks to heur
                    if state.board[i][j] == state.board[i][j + 1] == 2:
                        heur += 10
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 2:
                        heur += 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 2:
                        heur += 10000

                    # subtract player two streaks from heur
                    if state.board[i][j] == state.board[i][j + 1] == 1:
                        heur -= 10
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 1:
                        heur -= 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add player one streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 2:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 2:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 2:
                        heur += 10000

                    # add player two streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 1:
                        heur -= 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 1:
                        heur -= 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 2:
                        heur += 10
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 2:
                        heur += 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 2:
                        heur += 10000

                    # subtract player two streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 1:
                        heur -= 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 1:
                        heur -= 1000
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 1:
                        heur -= 100000
                except IndexError:
                    pass
        return heur

    def eval_p1(self, env):
        # ROW_COUNT = 6  # height
        # COLUMN_COUNT = 7  # width
        heur = 0
        state = deepcopy(env)
        for i in range(0, COLUMN_COUNT):
            for j in range(0, ROW_COUNT):
                try:
                    # add player one streak scores to heur
                    if state.board[i][j] == state.board[i + 1][j] == 2:
                        heur += 10
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 2:
                        heur += 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 2:
                        heur += 10000

                    # subtract player two streak score to heur
                    if state.board[i][j] == state.board[i + 1][j] == 1:
                        heur -= 10
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 1:
                        heur -= 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add player one vertical streaks to heur
                    if state.board[i][j] == state.board[i][j + 1] == 2:
                        heur += 10
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 2:
                        heur += 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 2:
                        heur += 10000

                    # subtract player two streaks from heur
                    if state.board[i][j] == state.board[i][j + 1] == 1:
                        heur -= 10
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 1:
                        heur -= 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add player one streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 2:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 2:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 2:
                        heur += 10000

                    # add player two streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 1:
                        heur -= 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 1:
                        heur -= 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 2:
                        heur += 10
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 2:
                        heur += 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 2:
                        heur += 10000

                    # subtract player two streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 1:
                        heur -= 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 1:
                        heur -= 1000
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 1:
                        heur -= 100000
                except IndexError:
                    pass
        return heur

    def minimax(self, env, move, max_depth):
        possible = env.topPosition >= 0
        max_v = -math.inf
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        for column in indices:
            child = self.simulateMove(deepcopy(env), column, self.position)
            v = self.MIN(child, max_depth - 1)
            if v > max_v:
                max_v = v
                move[:] = [column]


class alphaBetaAI(connect4Player):

    def play(self, env, move):
        if len(env.history[0]) == 0 or len(env.history[1]) == 0:
            move[:] = [3]
            print("first move finished")
            return
        self.minimax(deepcopy(env), move, 4)
        print("Finished!")

    def simulateMove(self, env, move, player):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)
        return env

    def MAX(self, env, depth, alpha, beta):
        if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape[1]:
            return 0
        if env.gameOver(env.history[0][-1], self.opponent.position):
            return -math.inf
        if depth == 0:
            if self.position == 1:
                return self.eval_p1(env)
            else:
                return self.eval(env)
        max_value = -math.inf
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        for move in indices:
            child = self.simulateMove(deepcopy(env), move, self.position)
            max_value = max(max_value, self.MIN(child, depth - 1, alpha, beta))
            alpha = max(alpha, max_value)
            if max_value >= beta:
                break
        return max_value

    def MIN(self, env, depth, alpha, beta):
        if len(env.history[0]) + len(env.history[1]) == env.board.shape[0] * env.board.shape[1]:
            return 0
        if env.gameOver(env.history[0][-1], self.position):
            return math.inf
        if depth == 0:
            if self.position == 1:
                return self.eval_p1(env)
            else:
                return self.eval(env)
        min_value = math.inf
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        for move in indices:
            child = self.simulateMove(deepcopy(env), move, self.opponent.position)
            min_value = min(min_value, self.MAX(child, depth - 1, alpha, beta))
            beta = min(beta, min_value)
            if min_value <= alpha:
                break
        return min_value

    def eval(self, env):
        # ROW_COUNT = 6  # height
        # COLUMN_COUNT = 7  # width
        heur = 0
        state = deepcopy(env)
        for i in range(0, COLUMN_COUNT):
            for j in range(0, ROW_COUNT):
                try:
                    # add player one streak scores to heur
                    if state.board[i][j] == state.board[i + 1][j] == 2:
                        heur += 10
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 2:
                        heur += 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 2:
                        heur += 10000

                    # subtract player two streak score to heur
                    if state.board[i][j] == state.board[i + 1][j] == 1:
                        heur -= 10
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 1:
                        heur -= 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add player one vertical streaks to heur
                    if state.board[i][j] == state.board[i][j + 1] == 2:
                        heur += 10
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 2:
                        heur += 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 2:
                        heur += 10000

                    # subtract player two streaks from heur
                    if state.board[i][j] == state.board[i][j + 1] == 1:
                        heur -= 10
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 1:
                        heur -= 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add player one streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 2:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 2:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 2:
                        heur += 10000

                    # add player two streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 1:
                        heur -= 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 1:
                        heur -= 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 1:
                        heur -= 10000
                except IndexError:
                    pass

                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 2:
                        heur += 10
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 2:
                        heur += 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 2:
                        heur += 10000

                    # subtract player two streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 1:
                        heur -= 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 1:
                        heur -= 1000
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 1:
                        heur -= 100000
                except IndexError:
                    pass
        return heur

    def eval_p1(self, env):
        # ROW_COUNT = 6  # height
        # COLUMN_COUNT = 7  # width
        heur = 0
        state = deepcopy(env)
        for i in range(0, COLUMN_COUNT):
            for j in range(0, ROW_COUNT):
                try:
                    # add player one streak scores to heur
                    if state.board[i][j] == state.board[i + 1][j] == 1:
                        heur += 10
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 1:
                        heur += 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 1:
                        heur += 10000

                    # subtract player two streak score to heur
                    if state.board[i][j] == state.board[i + 1][j] == 2:
                        heur -= 100
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == 2:
                        heur -= 1000
                    if state.board[i][j] == state.board[i + 1][j] == state.board[i + 2][j] == state.board[i + 3][
                        j] == 2:
                        heur -= 100000
                except IndexError:
                    pass

                try:
                    # add player one vertical streaks to heur
                    if state.board[i][j] == state.board[i][j + 1] == 1:
                        heur += 10
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 1:
                        heur += 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 1:
                        heur += 10000

                    # subtract player two streaks from heur
                    if state.board[i][j] == state.board[i][j + 1] == 2:
                        heur -= 100
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == 2:
                        heur -= 1000
                    if state.board[i][j] == state.board[i][j + 1] == state.board[i][j + 2] == state.board[i][
                        j + 3] == 2:
                        heur -= 100000
                except IndexError:
                    pass

                try:
                    # add player one streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 1:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 1:
                        heur += 100
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 1:
                        heur += 10000

                    # add player two streaks to heur
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == 2:
                        heur -= 1000
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] == 2:
                        heur -= 1000
                    if not j + 3 > ROW_COUNT and state.board[i][j] == state.board[i + 1][j + 1] == state.board[i + 2][
                        j + 2] \
                            == state.board[i + 3][j + 3] == 2:
                        heur -= 100000
                except IndexError:
                    pass

                try:
                    # add  player one streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 1:
                        heur += 10
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 1:
                        heur += 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 1:
                        heur += 10000

                    # subtract player two streaks
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == 2:
                        heur -= 100
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][
                        j - 2] == 2:
                        heur -= 1000
                    if not j - 3 < 0 and state.board[i][j] == state.board[i + 1][j - 1] == state.board[i + 2][j - 2] \
                            == state.board[i + 3][j - 3] == 2:
                        heur -= 100000
                except IndexError:
                    pass
        return heur

    def minimax(self, env, move, max_depth):
        possible = env.topPosition >= 0
        max_v = -math.inf
        alpha = -math.inf
        beta = math.inf
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        for column in indices:
            child = self.simulateMove(deepcopy(env), column, self.position)
            v = self.MIN(child, max_depth - 1, alpha, beta)
            alpha = max(alpha, v)
            if v > max_v:
                max_v = v
                move[:] = [column]


SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6    # height
COLUMN_COUNT = 7  # width

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
