# Ethan Sudman
# K-Means Clustering (used to categorize data)
# Written for my AI class
# pts - list of touples
# Each touple contains the coordinates of one point and may have more than 2 dimensions
# We can assume that the points are distributed randomly
# nclusters - desired number of clusters
# Returns: centers, iters
# centers - list of touples, where each touple is a cluster center
# iters - number of iterations needed

import copy
import math

centers = []
clusters = []
currClusters = []

def cluster(pts, nclusters):
	global centers, clusters, currClusters, iter

	for i in range(0, nclusters):
		# Add a center
		centers.append(pts[i])
		
		# Add a corrusponding cluster
		clusters.append([])

	iterations = recalc(pts, 1, nclusters)

	return centers, iterations

def doCenters(pts, nclusters):
        global centers, clusters, currClusters
        currClusters = copy.deepcopy(clusters)
        clusters = []
        for i in range(0, nClusters):
                clusters.append[[]]
                
        for cluster in currClusters:
                for pt in cluster:
                        i = getClosestCenter(pt)
                        clusters[i].append(pt)

def recalc(pts, iteration, nclusters):
        global centers, clusters, currClusters

        done = False

        # For each dimension
        for i in range(0, len(currClusters[0])):
                add = 0
                numbers = 0
                # For each center
                # This needs to be fixed
                for j in range(0, len(centers)):
                        add += currClusters[j][i]
                        numbers += 1
                average = add / numbers

                change = math.fabs(average - centers[j][i])

                if change < 0.01:
                        centers[j][i] = float(average)
                        done = True
                else:
                        centers[j][i] = float(average)
                        done = False
                        
        if not done and iteration < 1000:
                doCenters(pts, nclusters)
                recalc(pts, (iteration + 1), nclusters)
        else: return iteration

# Pass a list of numbers, get their average
def mean(numbers):
	sum = 0
	for number in numbers:
		sum += number

	return (sum / len(numbers))

def getClosestCenter(point):
	global centers
	# arbitrary starting point
	distance = float("infinity")

	currCenter = None

	# Get the distance from the point to each center
	for i in range(0, len(centers)):
		dist = 0
		
		# Come up with a total "distance sum" by adding up the distance between each point	
		# We don't care that the dimensions are different
		for j in range(0, len(point)):
			dist += center[i][j] - point[j]
		if dist < distance:
			distance = dist
			currCenter = center
	return i
