#!/usr/bin/python
#
#  Map data for astar problem.
#
#  The data file 'miles.dat' and the code for absorbing
#  this file were cribbed from the Stanford GraphBase project.
#  It contains 128 US and Canadian cities with map coordinates
#  and distances between them.
#
#  To this we added fake random road data in 'roads.dat'
#
#  adata.input()  Absorb the miles.dat file
#  adata.cities   A list of city names
#  adata.dist(city1, city2)  Ahe integer distance between 2 cities
#  adata.roads(city)  A list of adjacent (has road to) cities
#  adata.loc(city)  Returns (latitude, longitude) tuple for city
#  adata.scaledloc(city)  Returns (x-pos, y-pos) coordinates tuple
#                           scaled to the interval [0.0, 1.0]
#
import sys
import re

#  List of city names (strings)
#
cities = []

#  Matrix of distances: dists[city_1][city_2] = distance
#  It is a dictionary of dictionaries of integers
#
dists = {}

#  Locations: a dictionary of (latitude, longitude) of cities
#  indexed by city name.  The position is coded as 
#
locs = {}
scaledlocs = {}

#  Dictionary of roads from a city: roads[city1] = [city, city...]
#
roads = {}

#  Return the distance between two cities
#
def dist(c1, c2):
    return dists[c1][c2]

#  Return the road list from a city
def roadlist(c1):
    return roads[c1]

#  Return the latitude and longitude of a city.
#
def loc(c): return locs[c]
def scaledloc(c):  return scaledlocs[c]

#  Truncate the list of cities
#
def ncities(n):
    global cities, saved_cities, original_cities
    cities = original_cities[:n]
    saved_cities = cities[:]
    saved_cities.sort()
    
#  Read the city names and distances into the global variables
#
def input():
    global cities, dists, saved_cities, original_cities

    #  Read city and distances
    if len(cities) > 0: return
    fname = open("miles.dat", 'r')
    cityfind = re.compile(r'(?P<city>\D[^[]*)\[(?P<lat>\d*).(?P<lon>\d*)')
    for line in fname:
        if line.isspace() or line.startswith("*"): # skip comments
            continue
        m = cityfind.match(line)
        if m:   # Line has city name 
            i = 1
            city, lat, lon = m.group('city', 'lat', 'lon')
            cities.insert(0,city)
            dists[city]={ city : 0 }
            locs[city]=(int(lat), int(lon)) 
        else:                         # Line has distances to previous cities 
            for d in line.split():
                dists[city][cities[i]] = int(d)
                dists[cities[i]][city] = int(d)
                i=i+1
    fname.close()

    #  Read the roads file
    for city in cities:
        roads[city] = []
    fname = open("roads.dat", 'r')
    for line in fname:
        if line.isspace() or line.startswith("*"): # skip comments
            continue
        c1, c2 = line.strip().split('#')
        if (c1 in roads) and (c2 in roads) and not (c1 in roads[c2]):
            roads[c1].append(c2)
            roads[c2].append(c1)
            
    fname.close()
    
    # Find minimum and maximum latitude and longitude
    #
    lats, lons = zip(*locs.values())
    minlat, maxlat = degmin(min(lats)), degmin(max(lats))
    minlon, maxlon = degmin(min(lons)), degmin(max(lons))
    latspan = float(maxlat - minlat)
    lonspan = float(maxlon - minlon)

    #  Save scaled location for each city
    for (city, latlon) in locs.iteritems():
        lat, lon = latlon
        scaledlocs[city] = ( (degmin(lat)-minlat)/latspan,  \
                             (degmin(lon)-minlon)/lonspan )

#  Convert degrees and minutes into a single integer
#
def degmin(x):  return (x/100)*60+(x%60)
#  Quick and dirty main program to absorb the city data and
#  manually check.
#
if __name__ == '__main__':

    input()
    print "Index of cities"
    for city in cities: 
        print city
    while True:
        print "Type a city:"
        c1 = sys.stdin.readline().strip()
        if not c1: break
        print "Type another city:"
        c2 = sys.stdin.readline().strip()
        if not c2: break
        print 'c1=', loc(c1), ' c2=', loc(c2), ' dist=', dist(c1,c2)
        print 'Scaled Loc', c1, '=', scaledloc(c1)
        print 'roads from', c1, '=',  roads[c1]
