# Ethan Sudman
# CS 332
# Tuesday, February 12, 2008
# Minimax lab

def run_minimax(gametree):
	x = run(gametree, True)
	gametree.score = x.score

# Run method - does the actual work
# Curr: node (initially pass in root)
# onMin: whether we were just doing a min or max node - this is
# useful for figuring out what to do with the children at each level
def run(curr, onMin):
	bestNum = -100
	if onMin:
		bestNum = 100;
	bestNode = curr.children[0]
	for child in curr.children:
		# If it's an even level, we're interested in the min
		if (child.level % 2) == 0:
			# If we were just doing mins, re-init
			if not onMin:
				onMin = True
				bestNum = 100
			if child.score == '':
				# Make a recursive call to figure out
				# what the score is
				x = run(child, onMin)
				child.score = x.score
			if child.score < bestNum:
				bestNum = child.score
				bestNode = child

		# Otherwise we want the max
		else:
			if onMin:
				onMin = False
				bestNum = -100
			if child.score == '':
				# Make a recursive call to
				# figure out what the score is
				x = run(child, onMin)
				child.score = x.score
			if child.score >= bestNum:
				bestNum = child.score
				bestNode = child

	bestNode.best = True
	return bestNode

#  The Node class contains:
#    level (0=root)
#    score ('' = unvisited node)
#    terminal (None = interior node)
#    best (None = not selected as best)
#
class Node:
    def __init__(self, level, score='', terminal=None):
        self.children = []
        self.score = score
        self.level = level
        self.terminal = terminal
        self.best = None
    
    def toString(self):
        s = ""
        if self.terminal:
            return str(self.score)
        else:
            bestflag = ''
            if self.best: bestflag = '*'
            return str(self.score) + bestflag + '[ ' +\
                   ' '.join([z.toString() for z in self.children]) + '] '


