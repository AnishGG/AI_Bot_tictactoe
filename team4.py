import random
from time import time

INF = 1e10
class Team4:

	def __init__(self):
		
		self.time_limit = 15
		self.max_depth = 100
		self.time_out = 0
		self.depth = 6

	def move(self, board, old_move, flag):
		
		self.time_start = time()
		self.time_out = 0
		ret = random.choice(board.find_valid_move_cells(old_move))

		for i in xrange(3,self.max_depth+1):
			self.depth = i
			ret = self.alpha_beta(board, -INF, INF, 0, old_move, flag)
			if self.time_out == 1:
				break

		return ret


	def alpha_beta(self, board, alpha, beta, depth, old_move, flag):

		available_cells = board.find_valid_move_cells(old_move)
		random.shuffle(available_cells)

		if (flag == 'x'):
			ans = -INF, available_cells[0]
			for cell in available_cells:
				board.update(old_move, cell, flag)
				if (depth >= self.depth):
					ret = self.heuristic(board, old_move)
				else:
					ret = self.alpha_beta(board, alpha, beta, depth+1, cell, 'o')
				board.board_status[cell[0]][cell[1]] = '-'
				if (ret > ans[0]):
					ans = ret, cell
				ans = max(ans, ret)
				if (ans[0] >= beta):
					break
				alpha = max(alpha, ans[0])

			return ans

		elif (flag == 'o'):
			ans = INF, available_cells[0]
			for cell in available_cells:
				board.update(old_move, cell, flag)
				if (depth >= self.depth):
					ret = self.heuristic(board, old_move)
				else:
					ret = self.alpha_beta(board, alpha, beta, depth+1, cell, 'x')
				board.board_status[cell[0]][cell[1]] = '-'
				ans = min(ans, ret)
				if (ans[0] <= alpha):
					break
				beta = min(beta, ans[0])
			return ans

	def heuristic(self, board, old_move):

		return random.choice(board.find_valid_move_cells(old_move))