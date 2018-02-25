import random
from time import time
import copy

INF = 1e10
class Team4:

	def __init__(self):
		
		self.hash_map = [dict() for i in xrange(101)]
		self.hash_table = [[[0 for k in xrange(4)] for j in xrange(4*4)] for i in xrange(4*4)]  
		self.time_limit = 1
		self.max_depth = 3
		self.time_out = 0
		self.depth = 1
		#self.cell_weight = [6, 4, 4, 6, 4, 3, 3, 4, 4, 3, 3, 4, 6, 4, 4, 6]
		self.x_mapping = {'x':1, 'o':-1, 'd':0, '-':0}
		self.o_mapping = {'x':-1, 'o':1, 'd':0, '-':0}

	def move(self, board, old_move, flag):
		
		if (flag == 'x'):
			my_flag = 'x'
			opp_flag = 'o'
		else:
			my_flag = 'o'
			opp_flag = 'x'
		self.time_start = time()
		self.time_out = 0
		ret_cell = random.choice(board.find_valid_move_cells(old_move))
		tmp = copy.deepcopy(board.block_status)
		board.update(old_move, ret_cell, flag)
		ret_val = self.heuristic_t(board, old_move, 'x', 'o')
		board.board_status[ret_cell[0]][ret_cell[1]] = '-'
		board.block_status = copy.deepcopy(tmp)
		del tmp
		for i in xrange(1,self.max_depth+1):
			self.depth = i
			ret = self.alpha_beta(board, -INF, INF, 1, old_move, flag,0, 1)
			if (ret[0] > ret_val):
				ret_val = ret[0]
				ret_cell = ret[1]

			print "ret at i", i, " is ", ret_cell, "ret[0] is ", ret[0]
			if self.time_out == 1:
				break
		return ret_cell

	def alpha_beta(self, board, alpha, beta, depth, old_move, flag, hash_val, bonus):

		available_cells = board.find_valid_move_cells(old_move)
		if (len(available_cells) == 0):
			if (flag == 'x'):
				return -INF, (0, 0)
			else:
				return INF, (0, 0)
		random.shuffle(available_cells)

		if (flag == 'x'):
			tmp = copy.deepcopy(board.block_status)
			ans = -INF, available_cells[0]
			tmp_alpha = alpha
			ret = -INF, (0, 0)
			for cell in available_cells:
				if (time() - self.time_start >= self.time_limit):
					self.time_out = 1
					break

				board.update(old_move, cell, flag)
				if board.find_terminal_state()[0] == 'o':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = -INF, cell
					return ans
				elif board.find_terminal_state()[0] == 'x':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = INF, cell
					return ans

				elif (depth >= self.depth and len(board.find_valid_move_cells(old_move)) > 0):
##					print "PRT BOARD STATE"
##					board.print_board()
					ret = self.heuristic_t(board, old_move,'x', 'o'), cell
##					print "heur is ", ret[0]
				elif (depth < self.depth):
					ret = self.alpha_beta(board, tmp_alpha, beta, depth+1, cell, 'o', hash_val, bonus)

				board.board_status[cell[0]][cell[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				if (ret[0] > ans[0]):
					ans = ret[0], cell
				if (ans[0] >= beta):
					break
				tmp_alpha = max(tmp_alpha, ans[0])
			del tmp
			return ans

		elif (flag == 'o'):
			tmp = copy.deepcopy(board.block_status)
			ans = INF, available_cells[0]
			ret = INF, (0, 0)
			tmp_beta = beta
			for cell in available_cells:
				if (time() - self.time_start >= self.time_limit):
					self.time_out = 1
					break
				board.update(old_move, cell, flag)
				if board.find_terminal_state()[0] == 'x':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = INF, cell
				elif board.find_terminal_state()[0] == 'o':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = -INF, cell
					return ans
				elif (depth >= self.depth and len(board.find_valid_move_cells(old_move)) > 0):
##					print "PRT BOARD STATE:"
##					board.print_board()
					ret = self.heuristic_t(board, old_move,'x','o'), cell
##					print "heur is ", ret
				elif (depth < self.depth):
						ret = self.alpha_beta(board, alpha, tmp_beta, depth+1, cell, 'x', hash_val, 0)

				board.board_status[cell[0]][cell[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				if (ret[0] < ans[0]):
					ans = ret[0], cell
				if (ans[0] <= alpha):
					break
				tmp_beta = min(tmp_beta, ans[0])
			del tmp
			return ans

	def check_subboard_full(self, board, cell, flag):
		ok = 1
		block_x = cell[0]//4 
		block_y = cell[1]//4
		if (board.block_status[block_x][block_y] != flag):
			ok = 0
		return ok

	def heuristic_t(self, board, old_move, flag, opp_flag):
		board_score = [[1 for i in xrange(4)] for j in xrange(4)]
		opp_board_score = [[1 for i in xrange(4)] for j in xrange(4)]
		goodness = 0
		opp_goodness = 0
		for i in xrange(4):
			for j in xrange(4):
				if (board.block_status == flag):
					board_score[i][j] = 100
				elif (board.block_status == opp_flag):
					board_score[i][j] = 0
				else:
					board_score[i][j]= self.per_block_t(board, old_move, flag, opp_flag,i, j)
					if (board_score[i][j] == 0):
						board_score[i][j] = 1
				if (opp_board_score[i][j] == opp_flag):
					opp_board_score[i][j] = 100
				elif (board.block_status == flag):
					opp_board_score[i][j] = 0
				else:
					opp_board_score[i][j] = self.per_block_t(board, old_move, opp_flag, flag, i, j)
					if (opp_board_score[i][j] == 0):
						opp_board_score[i][j] = 1
##				print i, j, board_score[i][j], opp_board_score[i][j]
		for i in xrange(4):
			goodness += (board_score[i][0] * board_score[i][1] * board_score[i][2] * board_score[i][3])
			goodness += (board_score[0][i] * board_score[1][i] * board_score[2][i] * board_score[3][i])
			opp_goodness += (opp_board_score[i][0] * opp_board_score[i][1] * opp_board_score[i][2] * opp_board_score[i][3])
			opp_goodness += (opp_board_score[0][i] * opp_board_score[1][i] * opp_board_score[2][i] * opp_board_score[3][i])

		for i in xrange(2):
			for j in xrange(2):
				goodness += self.diam_board(i+1, j+1, board.board_status, flag, board_score)
				opp_goodness += self.diam_board(i+1, j+1, board.board_status, opp_flag, opp_board_score)
##		print "goodness ", goodness
##		print "opp_goodness", opp_goodness
		return goodness - opp_goodness

	def diam_board(self, cx, cy, board_status, flag, board_score):
		return board_score[cx][cy+1] * board_score[cx][cy-1] * board_score[cx + 1][cy] * board_score[cx - 1][cy]

	def per_block_t(self, board, old_move, flag, opp_flag, block_x, block_y):
##		print "blox ", block_x, "bloy ", block_y
		block_goodness = 0
		rowarr = [0, 0, 0, 0]
		colarr = [0, 0, 0, 0]
		for i in xrange(4):
			for j in xrange(4):
##				print board.board_status[4*block_x+i][4*block_y+j],
				if (board.board_status[4*block_x+i][4*block_y+j] == flag):
					rowarr[i] += 1
					colarr[j] += 1
				if (board.board_status[4*block_x+i][4*block_y+j] == opp_flag):
					rowarr[i] = -1000
					colarr[j] = -1000
##			print
		for i in xrange(4):
##			print "rowarr[",i,"] ", rowarr[i]
##			print "colarr[",i,"] ", colarr[i]
			if (rowarr[i] < 0):
				pass
			if (colarr[i] < 0):
				pass
			if (rowarr[i] == 1):
				block_goodness += 3
			if (rowarr[i] == 2):
				block_goodness += 9
			if (rowarr[i] == 3):
				block_goodness += 27
			if (rowarr[i] == 4):
				block_goodness += 100
			if (colarr[i] == 1):
				block_goodness += 3
			if (colarr[i] == 2):
				block_goodness += 9
			if (colarr[i] == 3):
				block_goodness +=27
			if (colarr[i] == 4):
				block_goodness += 100

		diam_weight = [[0, 0], [0, 0]]
		for i in xrange(2):
			for j in xrange(2):
				diam_weight[i][j] = self.cal_diam_weight_t(4*block_x + 1 + i, 4*block_y + 1 + j, board.board_status, flag, opp_flag)
				block_goodness += diam_weight[i][j]
		return block_goodness

	def cal_diam_weight_t(self, centre_x, centre_y, board_status, flag, unflag):
		cx = centre_x
		cy = centre_y
		mp = {}
		if (flag == 'x'):
			mp = self.x_mapping
		else:
			mp = self.o_mapping
		a = mp[board_status[cx][cy+1]] 
		b = mp[board_status[cx][cy-1]] 
		c = mp[board_status[cx + 1][cy]] 
		d = mp[board_status[cx - 1][cy]]
		counter = a + b + c + d
		diam_weight = 0
		if (counter == 1):
			diam_weight += 3
		if (counter == 2):
			diam_weight += 9
		if (counter == 3):
			diam_weight += 27
		if (counter == 4):
			diam_weight += 100
		if (a == -1 or b == -1 or c == -1 or d == -1):
			diam_weight = 0
		return diam_weight	
