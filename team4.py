import random
from time import time
import copy

INF = 1e10
class Team4:

	def __init__(self):
		
		self.time_limit = 15
		self.max_depth = 100
		self.time_out = 0
		self.depth = 6
		self.cell_weight = [6, 4, 4, 6, 4, 3, 3, 4, 4, 3, 3, 4, 6, 4, 4, 6]
		self.mapping = {'x':1, 'o':-1, 'd':0, '-':0}

	def move(self, board, old_move, flag):
		
		self.time_start = time()
		self.time_out = 0
		ret = random.choice(board.find_valid_move_cells(old_move))

		for i in xrange(3,self.max_depth+1):
			self.depth = i
			ret = self.alpha_beta(board, -INF, INF, 0, old_move, flag)
			if self.time_out == 1:
				break

		print board.print_board()
		print ret
		return ret[1][0], ret[1][1]


	def alpha_beta(self, board, alpha, beta, depth, old_move, flag):

		available_cells = board.find_valid_move_cells(old_move)
		random.shuffle(available_cells)
		# print available_cells

		if (flag == 'x'):
			tmp = copy.deepcopy(board.block_status)
			ans = -INF, available_cells[0]
			for cell in available_cells:
				if (time() - self.time_start >= self.time_limit):
					self.time_out = 1
					break
				# print cell
				board.update(old_move, cell, flag)
				# print "--------------------------------------------------BEFORE-----------------------------------------"
				# print board.print_board()
				if board.find_terminal_state()[0] == 'o':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					continue;
				elif board.find_terminal_state()[0] == 'x':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = INF, cell
					return ans
				elif (depth >= self.depth and len(board.find_valid_move_cells(old_move)) > 0):
					ret = self.heuristic(board, old_move)
				elif (depth < self.depth):
					ret = self.alpha_beta(board, alpha, beta, depth+1, cell, 'o')
				board.board_status[cell[0]][cell[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				# print "--------------------------------------------------AFTER-----------------------------------------"
				# print board.print_board()
				if (ret > ans[0]):
					ans = ret, cell
				if (ans[0] >= beta):
					break
				alpha = max(alpha, ans[0])

			return ans

		elif (flag == 'o'):
			tmp = copy.deepcopy(board.block_status)
			ans = INF, available_cells[0]
			for cell in available_cells:
				if (time() - self.time_start >= self.time_limit):
					self.time_out = 1
					break
				# print cell
				board.update(old_move, cell, flag)
				# print "--------------------------------------------------BEFORE-----------------------------------------"
				# print board.print_board()
				if board.find_terminal_state()[0] == 'x':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					continue;
				elif board.find_terminal_state()[0] == 'o':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = INF, cell
					return ans
				elif (depth >= self.depth and len(board.find_valid_move_cells(old_move)) > 0):
					ret = self.heuristic(board, old_move)
				elif (depth < self.depth):
					ret = self.alpha_beta(board, alpha, beta, depth+1, cell, 'x')
				board.board_status[cell[0]][cell[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				# print "--------------------------------------------------AFTER-----------------------------------------"
				# print board.print_board()
				if (ret < ans[0]):
					ans = ret, cell
				if (ans[0] <= alpha):
					break
				beta = min(beta, ans[0])
			return ans

	def heuristic(self, board, old_move):
		goodness = 0
		goodness += self.calc_single_blocks(board, old_move)
		goodness += self.calc_as_whole(board, old_move)
		return goodness

	def calc_single_blocks(self, board, old_move):
		block_goodness = 0
		for i in xrange(4):
			for j in xrange(4):
				block_goodness += self.calc_per_block(board, old_move, i, j)
                return block_goodness

        def cal_diam_weight(self, centre_x, centre_y, board_status):
                # For a single diamond
                cx = centre_x
                cy = centre_y
                mp = self.mapping
                a = mp[board_status[cx][cy+1]] 
                b = mp[board_status[cx][cy-1]] 
                c = mp[board_status[cx + 1][cy]] 
                d = mp[board_status[cx - 1][cy]]
                diam_weight = 10*(a + b + c + d)
                if(a == -1 or b == -1 or c == -1 or d == -1):
                    diam_weight = 0
                return diam_weight

	def calc_per_block(self, board, old_move, block_x, block_y):

		# For checking how good a row/col is
		row_weight = [10, 10, 10, 10]
		col_weight = [10, 10, 10, 10]
		for i in xrange(4):
			for j in xrange(4):
				mapping_val = self.mapping[board.board_status[4*block_x+i][4*block_y+j]]
                    # Yes, the below line will help in the overall case
                                # row_weight += mapping_val * self.cell_weight			probably will only help in case of overall block
                                if(row_weight[i] == 10):
                                        row_weight[i] += mapping_val * 10
                                if(col_weight[j] == 10):
                                        col_weight[j] += mapping_val * 10
				if (mapping_val == -1):
					row_weight[i] = 0
					col_weight[j] = 0
				row_weight[i] *= 3
				col_weight[j] *= 3

		# For checking how good diamond state is
                diam_weight = [[0, 0], [0, 0]]
                for i in range(2):
                    for j in range(2):
                        diam_weight[i][j] = self.cal_diam_weight(4*block_x + 1 + i, 4*block_y + 1 + j, board.board_status)

                return 0    ##############################have to change return for now ##################

	def calc_as_whole(self, board, old_move):

		# For checking how good a row/col is
		row_weight = [10, 10, 10, 10]
		col_weight = [10, 10, 10, 10]
		for i in xrange(4):
			for j in xrange(4):
				mapping_val = self.mapping[board.block_status[i][j]]
				row_weight += mapping_val * self.cell_weight			# probably will only help in case of overall block
                                if(row_weight[i] == 10):
                                        row_weight[i] += mapping_val * 10
                                if(col_weight[j] == 10):
                                        col_weight[j] += mapping_val * 10
				if (mapping_val == -1):
					row_weight[i] = 0
					col_weight[j] = 0
				row_weight[i] *= 3
				col_weight[j] *= 3

		# For checking how good diamond state is
                return 0    ##############################have to change return for now ##################
