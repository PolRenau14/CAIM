"""
.. module:: PageRank

PageRank
******

:Description: PageRank
    Compute a simulation page rank but with airports example.
    It's missing when one node is not connected ( no ones travel to him)


:Authors:
    Pol

:Version:
    1.0

:Date:
    07/11/2019
"""
#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None,desti=None,index=None):
        self.origin = origin # write appropriate value
        self.desti = desti
        self.weight = 1.0 # write appropriate value
        self.index = index

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None,pageIndex = None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0.0    # at first time we have 0. cause there no conneections with it
        self.pageIndex = pageIndex      # this value indicates the position of edgeList.

    def __repr__(self):
        return "{0}\t{2}\t{1}\t{3}".format(self.code, self.name, self.pageIndex,self.routes)

    def addRoute(self,e=Edge()):
        self.routes.append(e)
        self.routeHash[e.origin] = e

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match: clau Index.
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def getAirport(code):
    if code in airportHash:
        return airportHash[code]

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
            a.pageIndex=cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print("There were {0} Airports with IATA code".format(cont))


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd,"r")
    cont = 0
    for line in routesTxt.readlines():
        e = Edge()
        try:
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code on route')
            e.origin    = temp[2]
            e.desti     = temp[4]
            e.index     = cont
            airportOrigen = getAirport(e.origin)
            airportDesti = getAirport(e.desti)

            airportOrigen.outweight += 1.0
            airportDesti.addRoute(e)

        except Exception as inst:
            pass
        else:
            cont += 1
            edgeList.append(e)
            edgeHash[e.origin] = e
    routesTxt.close()
    print("There where {0} edges with IATA code".format(cont))
    # write your code

def makeDiff(v1,v2):
    dif = 0
    for i in range(0,len(v1)):
        dif += v1[i]-v2[i]
    return dif



def computePageRanks():
    # write your code
    print("ComputingPageRanks")
    n = len(airportList)
    P = [1/n for i in range(n)]
    L = 0.5                     # quan més gran és més iteracions realitza.
    thresHold = 0.00000000006
    dif = 1.0
    iterations = 0

    def getSum(i):
        sum = 0
        for eVal in airportList[i].routes:
            j = airportHash[eVal.origin].pageIndex
            aux = P[j] * eVal.weight / airportList[j].outweight
            sum += aux
        return sum

    while dif > thresHold :
        Q = [0 for i in range(n)]
        for i in range(0,n-1):
            Q[i] = L * getSum(i) + (1-L)/n
        dif = sum( [ p-q for (p,q) in zip(P,Q)])
        P = Q
        iterations += 1
    return iterations,P

def outputPageRanks(pageRanks):
    # write your code
    print("Output pageRanks")
    for i in range(0,len(pageRanks)):
        print(airportList[i]), print(pageRanks[i])


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations,pageRanks = computePageRanks()
    time2 = time.time()
    outputPageRanks(pageRanks)
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)

if __name__ == "__main__":
    sys.exit(main())
