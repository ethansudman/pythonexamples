import copy

class Konane:
    def __init__(self, board, who, print_board):
	self.who = who
	self.board = board
        self.print_board = print_board
	self.depth = 3

   # Figures out if a player (who) has any possible moves left
   # If not, game is done for them
    def gameDone(self, who):	
	possibleMoves = []
	for square in self.getEmpty(self.board):
		possibleMoves.extend(self.plausibleMoves(self.board, square, who))

	# They're done if they're out of possible moves
	if len(possibleMoves) == 0: return True
	else: return False

    # Make a particular move on a particular board
    # board: board we want to make the move on
    # move: move we want made
    # Warning: do NOT pass this method a pointer to the board, ONLY pass it the value!
    def makeMoveOnBoard(self, board, move):
	piece = copy.copy(board[move[0]][move[1]])
	board[move[0]][move[1]] = " "
	board[move[2]][move[3]] = piece
	
	# Clear captured piece
	# Move is to the left
	if move[0] > move[2]:
		board[(move[0] - 1)][move[1]] = " "
		# Handle double jumps
		if (move[0] - move[2]) == 4:
			board[(move[0] - 3)][move[1]] = " "
			
	# Move is to the right
	elif move[0] < move[2]:
		board[(move[0] + 1)][move[1]] = " "
		# Handle double jumps
		if (move[2] - move[0]) == 4:
			board[(move[0] + 3)][move[1]] = " "
	# Move upward
	elif move[1] > move[3]:
		board[move[0]][(move[1] - 1)] = " "
		if (move[1] - move[3]) == 4:
			board[move[0]][(move[1] - 3)] = " "

	# move downward
	elif move[1] < move[3]:
		board[move[0]][(move[1] + 1)] = " "
		if (move[3] - move[1]) == 4:
			board[move[0]][(move[1] + 3)] = " "
	return board

    def move(self):
	# Start by assigning them nothing
	bestScore = None
	bestMove = None
	possibilities = []
	for square in self.getEmpty(self.board):
		possibilities.extend(self.plausibleMoves(self.board, square, self.who))
	lenPossibilities = len(possibilities)
	for move in possibilities:
		futureMoves = self.getFuture(self.board, move, 0, self.opponent(self.who))
				
		# Select move if it's more favorable to me (i.e. most moves for me, fewest for opponent)
		if bestScore == None or futureMoves > bestScore:	
			bestScore = futureMoves
			bestMove = move
	
	return bestMove

    def getFuture(self, board, move, currDepth, who):
	newBoard = self.makeMoveOnBoard(copy.deepcopy(board), move)
	possibilities = []
	isMinStep = (currDepth % 2) == 0
	for square in self.getEmpty(newBoard):
		possibilities.extend(self.plausibleMoves(newBoard, square, who))
	lenPossibilities = len(possibilities)
	if lenPossibilities == 0 or self.depth == 0: return 0
	elif (self.depth - currDepth) == 1:
		if isMinStep: return (0 - lenPossibilities)
		else: return lenPossibilities
	elif isMinStep:
		best = None
		bestScore = 0
		for currMove in possibilities:
			future = self.getFuture(newBoard, currMove, (currDepth + 1), self.opponent(who))
			if best == None or future < bestScore:
				best = currMove
				bestScore = future
		return ((0 - lenPossibilities) + bestScore)
	else:
		best = None
		bestScore = 0
		for currMove in possibilities:
			future = self.getFuture(newBoard, currMove, (currDepth + 1), self.opponent(who))
			if best == None or future > bestScore:
				best = currMove
				bestScore = future
		return (lenPossibilities + future)
									
    # Get opponent	
    def opponent(self, who):
	if who == "x": return "o"
	elif who == "o": return "x"
	else: return "i"
	
    # Returns a list of empty spaces on a board	
    def getEmpty(self, board):
	empty = []
	for i in range(0, 8):
		for j in range(0, 8):
			if board[i][j] == " ":
				empty.append((i, j))
	return empty

    # Comes up with a list of plausible moves to a square
    # board: current board
    # square: empty square
    # who: player to move there
    def plausibleMoves(self, board, square, who):
		possibleMoves = []
		
		# Look to the left
		if square[0] > 1:
			# Make sure the two over is one of the players' pieces
			cond1 = board[(square[0] - 2)][square[1]] == who

			# Make sure square next to it is an opponents' piece
			# I.e. someone can't capture their own piece
			cond2 = board[(square[0] - 1)][square[1]] == self.opponent(who)

			# Check above mentioned conditions
			if cond1 and cond2:
				# Touple: current x, current y, x they're moving to, y they're moving to
				possibleMoves.append(((square[0] - 2), square[1], square[0], square[1]))

			elif square[0] > 4:
				cond3 = board[(square[0] - 4)][square[1]] == who
				cond4 = board[(square[0] - 3)][square[1]] == self.opponent(who)
				# "and not cond1" condition is implied in each of these cases
				if cond2 and cond3 and cond4:
					possibleMoves.append(((square[0] - 4), square[1], square[0], square[1]))
		
		# Look to the right
		if square[0] < 6:
			cond1 = board[(square[0] + 2)][square[1]] == who
			cond2 = board[(square[0] + 1)][square[1]] == self.opponent(who)
			
			if cond1 and cond2:
				possibleMoves.append(((square[0] + 2), square[1], square[0], square[1]))
			# Look for a double jump
			elif square[0] < 4:
				# Make sure it's one of our own pieces
				cond3 = board[(square[0] + 4)][square[1]] == who

				# Don't jump over own piece
				cond4 = board[(square[0] + 3)][square[1]] == self.opponent(who)
				cond5 = board[(square[0] + 2)][square[1]] == " "

				if cond2 and cond3 and cond4 and cond5:
					possibleMoves.append(((square[0] + 4), square[1], square[0], square[1]))
			
		# Look above
		if square[1] > 1:
			cond1 = board[square[0]][(square[1] - 2)] == who
			cond2 = board[square[0]][(square[1] - 1)] == self.opponent(who)

			if cond1 and cond2:
				possibleMoves.append((square[0], (square[1] - 2), square[0], square[1]))
			# These have conflicting conditions, so they can't possibly both be true
			elif square[1] > 4:
				cond3 = board[square[0]][(square[1] - 4)] == who
				cond4 = board[square[0]][(square[1] - 3)] == self.opponent(who)
				cond5 = board[square[0]][(square[1] - 2)] == " "
				if cond2 and cond3 and cond4:
					possibleMoves.append((square[0], (square[1] - 4), square[0], square[1]))

		# Look below
		if square[1] < 6:
			cond1 = board[square[0]][(square[1] + 2)] == who
			cond2 = board[square[0]][(square[1] + 1)] == self.opponent(who)

			if cond1 and cond2:
				possibleMoves.append((square[0], (square[1] + 2), square[0], square[1]))
			elif square[1] < 4:
				cond3 = board[square[0]][(square[1] + 2)] == " "
				cond4 = board[square[0]][(square[1] + 3)] == self.opponent(who)
				cond5 = board[square[0]][(square[1] + 2)] == who
				if cond2 and cond3 and cond4 and cond5:
					possibleMoves.append((square[0], (square[1] + 4), square[0], square[1]))
				
		return possibleMoves
		