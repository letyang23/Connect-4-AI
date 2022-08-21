import numpy as np
import random
import sys
import signal
from players import connect4Player
from copy import deepcopy

class monteCarloAI(connect4Player):

	def play(self, env, move):
		random.seed(self.seed)
		# Find legal moves
		env = deepcopy(env)
		env.visualize = False
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		# Init fitness trackers
		vs = np.zeros(7)
		# Play until told to stop
		counter = 0
		while counter < 1000:
			first_move = random.choice(indices)
			turnout = self.playRandomGame(deepcopy(env), first_move)
			if turnout == self.position:
				vs[first_move] += 1
			elif turnout != 0:
				vs[first_move] -= 1
			if counter % 100 == 0:
				move[:] = [np.argmax(vs)]
			counter += 1
		move[:] = [np.argmax(vs)]

	def playRandomGame(self, env, first_move):
		switch = {1:2,2:1}
		move = first_move
		player = self.position
		self.simulateMove(env, move, player)
		while not env.gameOver(move, player):
			player = switch[player]
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			move = random.choice(indices)
			self.simulateMove(env, move, player)
		if len(env.history[0]) == 42: return 0
		return player

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)

	def signal_handler(self):
		print("SIGTERM ENCOUNTERED")
		sys.exit(0)


# provided code in the video
def MAX(state, depth):
	if gameover(state) or depth == 0:
		return eval(state)
	possible = env.topPosition >= 0
	max_v = -inf
	for move in possible:
		child = simulateMove(deepcopy(env), move, self.opponent.position)
		max_v = max(max_v, MIN(child, depth-1))
	return max_v


def MIN(state, depth):
	if gameover(state) or depth == 0:
		return eval(state)
	possible = env.topPosition >= 0
	min_v = inf
	for move in possible:
		child = simualteMove(deepcopy(env), move, self.opponent.position)
		min_v = min(min_v, MAX(child, depth-1))
	return min_v


# evaluation function
def eval(state):
	...


def Minimax(env, max_depth):
	possible = env.topPosition >= 0
	max_v = -inf
	for move in possible:
		child = simulateMove(deepcopy(env), move, self.opponent.position)
		v = MIN(child, depth-1)
		if v > max_v:
			max_v = v
			move[:] = [move]
	return move


def iterativeDeepening(state):
	limit = 1
	while(True):
		move[:] = [Minimax(original_state, limit)]
		limit += 1