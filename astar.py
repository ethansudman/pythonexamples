#  Ethan Sudman
#  A* path finding class
#  Written for my AI class
#  The Node class and the AS class are called by
#  the driver program

import copy
import adata

class AS:
    def __init__(self, startcity, goalcity, tracefunc):
        self.startcity = startcity
        self.goalcity = goalcity
        self.tracefunc = tracefunc
        
	# F and H for the first node (they're the same)
	fandh = adata.dist(self.startcity, self.goalcity)
        
	# Currently open nodes
	self.openlist = [Node([startcity], fandh, 0, fandh)]

        # Visited nodes
        self.closedlist = []

    # Gets the index of the node on the openlist with
    # the lowest f function
    def getLowest(self):
	lowestF = -1
	lowestIndex = -1
	for i in range(0, len(self.openlist)):
		if lowestF == -1:
			lowestF = self.openlist[i].f
			lowestIndex = i
		elif self.openlist[i].f < lowestF:
			lowestF = self.openlist[i].f
			lowestIndex = i
	return lowestIndex

    # Main loop
    # Debugging options: "trace" turns trace on and off
    def astar_run(self, dbg):
	if dbg == "bfs":
		while 0 < 1:
			curr = self.bfs(dbg)
			if curr == "Not done":
				continue
			elif curr == "Not found":
				# Driver interprets this as "not found"
				return None
			# Else it's a node
			else:
				return curr
				
	else:
        	# The first time, run it by popping
	        # the last item off the openlist
		self.actual_run(-1, dbg)

	        # Afterwards, do it for the index of the one
        	# we determine to have the smallest f function
	        # We do this until we're done
        	while 0 < 1:
		    lowest = self.getLowest()
		    # See if we're done
		    if self.openlist[lowest].path[-1] == self.goalcity:
			if self.tracefunc:
				self.tracefunc(self.openlist[lowest])	
			return self.openlist[lowest]
	            else:
        	    	self.actual_run(lowest, dbg)

    # Does most of the actual work
    def actual_run(self, index, dbg):
        # Remove and return the last node
        currNode = self.openlist.pop(index)

	# See if we have any debugging options
	if self.tracefunc:
		self.tracefunc(currNode)

        # Add it to the closed node list
        self.closedlist.append(currNode)

        # I want the last city on the path
        # This is where we "are" currently
        currCity = currNode.path[-1]

        # Figure out where we can go from here
        possibleCities = adata.roadlist(currCity)

        # f function of the lowest node
        # Start w/ -1 so we can know it hasn't been touched yet
        lowestF = -1

        # Index of the lowest node
        lowestIndex = -1

        # Loop through the possibilies
        for city in possibleCities:
	    # The new path is the path of the open node plus the current city
            newPath = copy.deepcopy(currNode.path)
            newPath.append(city)

	    # Get the g, h, and f functions
	    # g is the g of the previous node plus the distance
    	    # between the last city on its path and the current city
    	    g = 0
    	    if not dbg == "h":
                g = currNode.g + adata.dist(currNode.path[-1], city)
	    h = adata.dist(city, self.goalcity)
	    f = g + h
	    
	    # Create the new node
            newNode = Node(newPath, f, g, h)

            # Add it to the open list
            self.openlist.append(newNode)

    def contains(self, cityList, seeking):
        for city in cityList:
            if city == seeking:
                return True
        return False
        
    def bfs(self, dbg):
	# If the list is empty
	if self.openlist == []:
		return "Not found"

	# We can just use the openlist as a queue - no point in making a new data structure
	currNode = self.openlist.pop(0)
	if self.tracefunc:
		self.tracefunc(currNode)

	# If this is the goal, return it
	if currNode.path[-1] == self.goalcity:
		return currNode

	possibleCities = adata.roadlist(currNode.path[-1])
	for city in possibleCities:
                # Make sure we don't get redundant things on here
                if self.contains(currNode.path, city):
                    continue
		currPath = copy.deepcopy(currNode.path)
		currPath.append(city)
		g = currNode.g + adata.dist(currNode.path[-1], city)
		# We use no h function by definition, so f = g and h = 0
		self.openlist.append(Node(currPath, g, g, 0))
		
	return "Not done"
class Node:
    # f = f function, g = g function, h = h funcion
    # path = everything we visited to get to that function
    def __init__(self, path, f, g, h):
        self.path = path[:]
        self.f = f
        self.g = g
        self.h = h

    def toString(self):
        s = 'f=%d g=%d h=%d ' % (self.f, self.g, self.h)
        for city in self.path:
            s = s + ' ' + city
        return s
        

