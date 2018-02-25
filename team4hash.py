import random
from time import time
import copy

INF = 1e10
class Team4:

	def __init__(self):
		
		self.hash_map = [dict() for i in xrange(101)]
		self.hash_table = [[[0 for k in xrange(4)] for j in xrange(4*4)] for i in xrange(4*4)]  
		self.time_limit = 15
		self.max_depth = 100
		self.time_out = 0
		self.depth = 6
		self.init_hash_table()
		self.cell_weight = [6, 4, 4, 6, 4, 3, 3, 4, 4, 3, 3, 4, 6, 4, 4, 6]
		self.x_mapping = {'x':1, 'o':-1, 'd':0, '-':0}
		self.o_mapping = {'x':-1, 'o':1, 'd':0, '-':0}

	def index(self,pos):
		if (pos == 'x'):
			return 1
		elif (pos == 'o'):
			return 2
		else:
			return 3

	def init_hash_table(self):
		for i in xrange(4*4):
			for j in xrange(4*4):
				for k in xrange(4):
					self.hash_table[i][j][k] = random.randrange(1, 2**34)

	def compute_hash(self, board):
		ret = 0
		for i in xrange(4*4):
			for j in xrange(4*4):
				ret ^= self.hash_table[i][j][self.index(board.board_status[i][j])]
		return ret

	def move(self, board, old_move, flag):
		
		self.time_start = time()
		self.time_out = 0
		ret_cell = random.choice(board.find_valid_move_cells(old_move))
		tmp = copy.deepcopy(board.block_status)
		board.update(old_move, ret_cell, flag)
##		print "current board"
##		board.print_board()
		ret_val = self.heuristic(board, old_move, flag)
		board.board_status[ret_cell[0]][ret_cell[1]] = '-'
		board.block_status = copy.deepcopy(tmp)
		del tmp
		for i in xrange(101):
			self.hash_map[i].clear()
		for i in xrange(1,self.max_depth+1):
			self.depth = i
			hash_val = self.compute_hash(board)
			ret = self.alpha_beta(board, -INF, INF, 0, old_move, flag, hash_val, 1)
			if (ret[0] > ret_val):
				ret_val = ret[0]
				ret_cell = ret[1]

			print "ret at i", i, " is ", ret_cell
			# print "hash_map is ", self.hash_map
			if self.time_out == 1:
				break

##		print board.print_board()
		# print ret
		return ret_cell


	def alpha_beta(self, board, alpha, beta, depth, old_move, flag, hash_val, bonus):

		# print "last move", old_move
		available_cells = board.find_valid_move_cells(old_move)
		if (len(available_cells) == 0):
			if (flag == 'x'):
				return -INF, (0, 0)
			else:
				return INF, (0, 0)
		random.shuffle(available_cells)
		# print available_cells
		# print available_cells

		if (flag == 'x'):
			tmp = copy.deepcopy(board.block_status)
			ans = -INF, available_cells[0]
			tmp_alpha = alpha
			ret = -INF, (0, 0)
			for cell in available_cells:
				hash_val ^= self.hash_table[cell[0]][cell[1]][self.index('-')]
				hash_val ^= self.hash_table[cell[0]][cell[1]][self.index('x')]
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
					ans = -INF, cell
					return ans
				elif board.find_terminal_state()[0] == 'x':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = INF, cell
					return ans
				elif (depth >= self.depth and len(board.find_valid_move_cells(old_move)) > 0):
##					print "board state:"
##					board.print_board()
					if hash_val in self.hash_map[depth]:
						print "FOUND IN HASH_MAP"
						ret = self.hash_map[depth][hash_val], cell
					else:
						ret = self.heuristic(board, old_move,'x'), cell
###						board.board_status[cell[0]][cell[1]] = 'o'
##						print "checking if o move"
##						board.print_board()
###						ret2 = self.heuristic(board, old_move,'o')
###						board.board_status[cell[0]][cell[1]] = 'x'
###						ret = ret1 + ret2, cell
						self.hash_map[depth][hash_val] = ret[0]
##					print "flag is ",flag
##					print ret
					# board.print_board()
					# print "ret is ", ret
				elif (depth < self.depth):
					ok = self.check_subboard_full(board, cell, flag)
					if (ok == 1 and bonus == 1):
						ret = self.alpha_beta(board, tmp_alpha, beta, depth+1, cell, 'o', hash_val, 0)
					else:
						ret = self.alpha_beta(board, tmp_alpha, beta, depth+1, cell, 'x', hash_val, bonus)

				board.board_status[cell[0]][cell[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				# print "--------------------------------------------------AFTER-----------------------------------------"
				# print board.print_board()
				### print "ret[0] here is ", ret[0]
				if (ret[0] > ans[0]):
				##	# print "ret[0] ", ret[0], "cell ", cell
					ans = ret[0], cell
				if (ans[0] >= beta):
					break
				tmp_alpha = max(tmp_alpha, ans[0])
			### print "ans is ", ans, " flag ", flag , " depth ", depth
			del tmp
			return ans

		elif (flag == 'o'):
			tmp = copy.deepcopy(board.block_status)
			ans = INF, available_cells[0]
			ret = INF, (0, 0)
			tmp_beta = beta
			for cell in available_cells:
				hash_val ^= self.hash_table[cell[0]][cell[1]][self.index('-')]
				hash_val ^= self.hash_table[cell[0]][cell[1]][self.index('o')]
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
					ans = INF, cell
				elif board.find_terminal_state()[0] == 'o':
					board.board_status[cell[0]][cell[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					ans = -INF, cell
					return ans
				elif (depth >= self.depth and len(board.find_valid_move_cells(old_move)) > 0):
##					print "board state:"
##					board.print_board()
					if hash_val in self.hash_map[depth]:
						print "FOUND IN HASH_MAP"
						ret = self.hash_map[depth][hash_val], cell
					else:
						ret = self.heuristic(board, old_move,'x'), cell
###						board.board_status[cell[0]][cell[1]] = 'x'
##						print "board checking if X move"
##						board.print_board()
###						ret2 = self.heuristic(board, old_move,'x')
###						board.board_status[cell[0]][cell[1]] = 'o'
###						ret = -(ret1 + ret2), cell
						self.hash_map[depth][hash_val] = ret[0]					
##					print "flag is ", flag
##					print self.heuristic(board, old_move, 'o')
##					print self.heuristic(board, old_move, 'x')
##					print ret
						# board.print_board()
					# print "ret is ", ret					
				elif (depth < self.depth):
					ok = self.check_subboard_full(board, cell, flag)
					if (ok == 1 and bonus == 1):
						ret = self.alpha_beta(board, alpha, tmp_beta, depth+1, cell, 'o', hash_val, 0)
					else:
						ret = self.alpha_beta(board, alpha, tmp_beta, depth+1, cell, 'x', hash_val, bonus)

				board.board_status[cell[0]][cell[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				# print "--------------------------------------------------AFTER-----------------------------------------"
				# print board.print_board()
			###	print "ret[0] here is ", ret[0]
				if (ret[0] < ans[0]):
					ans = ret[0], cell
				if (ans[0] <= alpha):
					break
				tmp_beta = min(tmp_beta, ans[0])
			###print "ans is ", ans, " flag ", flag , " depth ", depth
			del tmp
			return ans

	def check_subboard_full(self, board, cell, flag):
		ok = 1
		block_x = cell[0]//4 
		block_y = cell[1]//4
		for i in xrange(4):
			for j in xrange(4):
				if (board.board_status[block_x+i][block_y+j] != flag):
					ok = 0
		return ok

	def heuristic(self, board, old_move, flag):
		goodness = 0
		goodness += self.calc_single_blocks(board, old_move, flag)
		goodness += (self.calc_as_whole(board, old_move, flag)*160)
		# print "goodness is ", goodness
		return goodness

	def calc_single_blocks(self, board, old_move, flag):
		
		block_goodness = 0
		for i in xrange(4):
			for j in xrange(4):
				block_goodness += self.calc_per_block(board, old_move, i, j, flag)
		return block_goodness

	def cal_diam_weight(self, centre_x, centre_y, board_status, flag):
		
		# For a single diamond
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
		# print "a b c d", a , b, c, d
		diam_weight = 3
		if (a == 1):
			diam_weight *= 20
		if (b == 1):
			diam_weight *= 20
		if (c == 1):
			diam_weight *= 20
		if (d == 1):
			diam_weight *= 20
		if(a == -1 or b == -1 or c == -1 or d == -1):
			diam_weight = 0
		if (diam_weight == 3):
			diam_weight = 0
		return diam_weight

	def calc_per_block(self, board, old_move, block_x, block_y, flag):

		ret = 0
		# For checking how good a row/col is
		row_weight = [3, 3, 3, 3]
		col_weight = [3, 3, 3, 3]
		for i in xrange(4):
			for j in xrange(4):
				# print board.board_status[4&block_x+i][4*block_y+j],
				if (flag == 'x'):
					mp = self.x_mapping
				else:
					mp = self.o_mapping
				mapping_val = mp[board.board_status[4*block_x+i][4*block_y+j]]
					# Yes, the below line will help in the overall case
								# row_weight += mapping_val * self.cell_weight			probably will only help in case of overall block
				if(row_weight[i] == 3):
					row_weight[i] += mapping_val * 5
				if(col_weight[j] == 3):
					col_weight[j] += mapping_val * 5
				if (mapping_val == -1):
					row_weight[i] = 0
					col_weight[j] = 0
				if (row_weight[i] != 3 and mapping_val != 0):
					row_weight[i] *= 16
				if (col_weight[j] != 3 and mapping_val != 0):
					col_weight[j] *= 16
			# print

		# For checking how good diamond state is
		diam_weight = [[3, 3], [3, 3]]
		for i in xrange(2):
			for j in xrange(2):
				diam_weight[i][j] = self.cal_diam_weight(4*block_x + 1 + i, 4*block_y + 1 + j, board.board_status, flag)
				# print "diam_weight ", i, j, " is ", diam_weight[i][j]
				ret += diam_weight[i][j]
##				print "diam_weight[i][j] ", diam_weight[i][j]
		for i in xrange(4):
##			print "rowweight[i] ",row_weight[i]
##			print "colweight[i] ", col_weight[i]
			# print "row_weight ", i, " is ", row_weight[i]
			# print "col_weight ", i, " is ", col_weight[i]
			if (row_weight[i] != 3):			
				ret += row_weight[i]
			if (col_weight[i] != 3):
				ret += col_weight[i]
##		print "blockx ", block_x, " block_y ", block_y, " perblock ", ret
		return ret   


	def calc_as_whole(self, board, old_move, flag):

		ret = 0
		# For checking how good a row/col is
		row_weight = [3, 3, 3, 3]
		col_weight = [3, 3, 3, 3]
		mp = {}
		for i in xrange(4):
			for j in xrange(4):
				if (flag == 'x'):
					mp = self.x_mapping
				else:
					mp = self.o_mapping
				mapping_val = mp[board.block_status[i][j]]
				row_weight += mapping_val * self.cell_weight			# probably will only help in case of overall block
				if(row_weight[i] == 3):
					row_weight[i] += mapping_val * 5
				if(col_weight[j] == 3):
					col_weight[j] += mapping_val * 5
				if (mapping_val == -1):
					row_weight[i] = 0
					col_weight[j] = 0
				if (row_weight[i] != 3 and mapping_val != 0):
					row_weight[i] *= 16
				if (col_weight[j] != 3 and mapping_val != 0):
					col_weight[j] *= 16

		# For checking how good diamond state is
		diam_weight = [[0, 0], [0, 0]]
		for i in xrange(2):
			for j in xrange(2):
				diam_weight[i][j] = self.cal_diam_weight(i, j, board.block_status, flag)
				ret += diam_weight[i][j]
		for i in xrange(4):
##			print "row_weight[i] ", row_weight[i]
##			print "col_weight[i] ", col_weight[i]
			if (row_weight[i] != 3):
				ret += row_weight[i]
			if (col_weight[i] != 3):
				ret += col_weight[i]
##		print "as a whole ", ret
		return ret