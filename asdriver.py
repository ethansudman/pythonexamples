
#  CS 332 A* Lab Command Line Driver
#
#  It is the student's responsibility to provide
#  file astar.py with class AS and method astar_run.
#
#  File adata provides access to the map data.
#
import adata   # Map data
import astar   # A* class
import sys

def printnode(n):
    print n.toString()
    
adata.input()

startcity = raw_input("Start city: ").strip()
if startcity not in adata.cities:
    print "City not recognized"
    sys.exit(0)

goalcity = raw_input("Goal city: ").strip()
if goalcity not in adata.cities:
    print "City not recognized"
    sys.exit(0)

dbg = raw_input("Debug Options: ").strip()

findpath = astar.AS(startcity, goalcity, printnode)

ans = findpath.astar_run(dbg)
if not ans:
    print "No answer"
else:
    print "Final Path:"
    print ans.toString()
    
        
