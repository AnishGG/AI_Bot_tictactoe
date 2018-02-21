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

		for i in range(3,max_depth+1):
			self.depth = i
			ret = self.alpha_beta(board, -INF, INF, i, old_move, flag)
			if self.time_out == 1:
				break

		return ret


	def alpha_beta(self, board, alpha, beta, depth, old_move, flag):

		available_cells = board.find_valid_move_cells(old_move)
		random.shuffle(available_cells)

		if (flag == 'x'):
			ans = -INF
			for cell in available_cells:
				board.update(old_move, cell, flag)
				ret = alpha_beta(board, alpha, beta, depth+1, cell, 'o')
				ans = max(ans, ret)
				if (ans >= beta):
					return ans
				alpha = max(alpha, ans)
			return ans

		if (flag == 'o'):
			ans = INF
			for cell in available_cells:
				board.update(old_move, cell, flag)
				ret = alpha_beta(board, alpha, beta, depth+1, cell, 'x')
				ans = min(ans, ret)
				if (ans <= alpha):
					return ans
				alpha = min(alpha, ans)
			return ans