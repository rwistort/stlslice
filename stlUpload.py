#! /usr/bin/env python

import string
import os
import sys
import collections
from pyx import *




#stlObject
#stl = stlObject(fileName)
#stl.printCoords()
#stl.maxDimensions()
#stl.rotate([x y z], angle)
#stl.scale(scalingFactor)
#stl.Translate([x y z])
#stl.getStlList() [[x y z][x y z]]




class stlObject:

    def __init__(self, filename):    
     

        f = open(filename, 'r')

        self.A = 0
        self.B = 0
        self.C = 0
        self.vertexCount = 0
        self.triangleList = []

        try:
            for line in f:
                if string.find(line, 'vertex') != -1:
                    L = string.split(line)
                    V = [float(L[1]), float(L[2]), float(L[3])]
                    if self.vertexCount == 0:
                        self.A = V
                        self.vertexCount += 1
                    elif self.vertexCount == 1:
                        self.B = V
                        self.vertexCount += 1
                    else:
                        self.C = V
                        self.vertexCount = 0
                        s = [self.A, self.B, self.C]
                        self.triangleList.append(s)
        finally:
            f.close()


    def printAllTriangles(self):
        for t in self.triangleList:
            print "point A: ", t[0]
            print "point B: ", t[1]
            print "point C: ", t[2]
            print " "


    # Find min and max values for x, y, z for stl model
    # return format is list:
    # [xMin, xMax, yMin, yMax, zMin, zMax]
    def boundingDimensions(self):
        xMin = 10000000
        xMax = -10000000
        yMin = 10000000
        yMax = -10000000
        zMin = 10000000
        zMax = -10000000

        for t in self.triangleList:
            for p in t:
                x = p[0]
                y = p[1]
                z = p[2]
                if x < xMin: xMin = x
                if x > xMax: xMax = x
                if y < yMin: yMin = y
                if y > yMax: yMax = y
                if z < zMin: zMin = z
                if z > zMax: zMax = z

        return [xMin, xMax, yMin, yMax, zMin, zMax]


#stlProcess()
#stlP.computelayerList(z, stlObject)
#tlP.saveLayerListPDF(layerList, fileName)
#stlP.saveLayerListEPS(layerList, fileName)
#stlP.saveLayerListJPEG(layerList, fileName)













class stlVector:
     def __init__(self, X, Y, Z):    
        self.X = X
        self.Y = Y
        self.Z = Z
    
class stlTriangle:
    def __init__(self, N, A, B, C):    
        self.N = N
        self.A = A
        self.B = B
        self.C = C

    def printTriangle(self):
        print "triangle Normal: ", self.N.X, " ", self.N.Y, " ", self.N.Z
        print "virtex 1: ", self.A.X, " ", self.A.Y, " ", self.A.Z
        print "virtex 2: ", self.B.X, " ", self.B.Y, " ", self.B.Z
        print "virtex 3: ", self.C.X, " ", self.C.Y, " ", self.C.Z
        print " "

class lineSegment:
     def __init__(self, X1, Y1, X2, Y2):    
        self.X1 = X1
        self.Y1 = Y1
        self.X2 = X2
        self.Y2 = Y2


class stlModel:

    def __init__(self, filename):    
     

        f = open(filename, 'r')

        self.vertexCount = 0
        self.N = 0
        self.A = 0
        self.B = 0
        self.C = 0

        self.triangleList = []

        try:
            for line in f:
                if string.find(line, 'normal') != -1:
                    L = string.split(line)
                    self.N = stlVector(float(L[2]), float(L[3]), float(L[4]))
              
                if string.find(line, 'vertex') != -1:
                    L = string.split(line)
                    V = stlVector(float(L[1]), float(L[2]), float(L[3]))
                    if self.vertexCount == 0:
                        self.A = V
                        self.vertexCount += 1
                    elif self.vertexCount == 1:
                        self.B = V
                        self.vertexCount += 1
                    else:
                        self.C = V
                        self.vertexCount = 0
                        s = stlTriangle(self.N, self.A, self.B, self.C)
                        self.triangleList.append(s)
        finally:
            f.close()


    def printAllTriangles(self):
        for t in self.triangleList:
            t.printTriangle()


    def findMinAndMazZ(self):
        minZ = 500
        maxZ = -500
        for t in self.triangleList:
            if t.A.Z < minZ:
                minZ = t.A.Z 
            if t.B.Z < minZ:
                minZ = t.B.Z 
            if t.C.Z < minZ:
                minZ = t.C.Z 
            if t.A.Z > maxZ:
                maxZ = t.A.Z 
            if t.B.Z > maxZ:
                maxZ = t.B.Z 
            if t.C.Z > maxZ:
                maxZ = t.C.Z 

        print "min Z value: ", minZ
        print "maz Z value: ", maxZ




    def findMidPoint(self, TopPt, BottomPt, z):

        l = []
        u  = (z - BottomPt.Z)/(TopPt.Z - BottomPt.Z)
        x = BottomPt.X + (u * (TopPt.X - BottomPt.X)) 
        y = BottomPt.Y + (u * (TopPt.Y - BottomPt.Y)) 
        l.append(x)
        l.append(y)
        return l


    # given a list of points and two more, add a bunch of points between the two...
    def addPointsInMiddle(self, listToBuild, start, end, gridSpace):
        
        xd = start[0] - end[0]
        yd = start[1] - end[1]
        d = ((xd ** 2) + (yd ** 2)) ** 0.5
        n = d / gridSpace
        count = 1
        while count < n:
            x = end[0] + (xd * (count/n))
            y = end[1] + (yd * (count/n))
            listToBuild.append([x, y])
            count += 1


    # given a list of points and single point find the closest point in list
    # pull out the point and return it
    def yankNearestN(self, workingList, point):
               
        dMax = 5000000.0
        countOfMin = 0
        xOfMin = 0.0
        yOfMin = 0.0

        for p in workingList:
            xd = point[0] - p[0]
            yd = point[1] - p[1]
            d = ((xd ** 2) + (yd ** 2)) ** 0.5
            if d < dMax:
                dMax = d
                xOfMin = p[0]
                yOfMin = p[1]

        workingList.remove([xOfMin, yOfMin])
        return [xOfMin, yOfMin]

    # Find a cross section of the 3d model using this hack

    def computeLayer(self, z, gridSpace, fileName):


        pointList = []
        for t in self.triangleList:

            # Point A up
            if t.A.Z > z and t.B.Z < z and t.C.Z < z :
                a = self.findMidPoint(t.A, t.B, z)
                b = self.findMidPoint(t.A, t.C, z)
                pointList.append(a)
                pointList.append(b)
                self.addPointsInMiddle(pointList, a, b, gridSpace)

            # Point B up
            elif t.B.Z > z and t.A.Z < z and t.C.Z < z :
                a = self.findMidPoint(t.B, t.A, z)
                b = self.findMidPoint(t.B, t.C, z)
                pointList.append(a)
                pointList.append(b)
                self.addPointsInMiddle(pointList, a, b, gridSpace)

            # Point C up
            elif t.C.Z > z and t.B.Z < z and t.A.Z < z :
                a = self.findMidPoint(t.C, t.A, z)
                b = self.findMidPoint(t.C, t.B, z)
                pointList.append(a)
                pointList.append(b)
                self.addPointsInMiddle(pointList, a, b, gridSpace)

            # Point A Down
            elif t.A.Z < z and t.B.Z > z and t.C.Z > z :
                a = self.findMidPoint(t.B, t.A, z)
                b = self.findMidPoint(t.C, t.A, z)
                pointList.append(a)
                pointList.append(b)
                self.addPointsInMiddle(pointList, a, b, gridSpace)

            # Point B Down
            elif t.B.Z < z and t.A.Z > z and t.C.Z > z :
                a = self.findMidPoint(t.A, t.B, z)
                b = self.findMidPoint(t.C, t.B, z)
                pointList.append(a)
                pointList.append(b)
                self.addPointsInMiddle(pointList, a, b, gridSpace)

            # Point C Down
            elif t.C.Z < z and t.B.Z > z and t.A.Z > z :
                a = self.findMidPoint(t.B, t.C, z)
                b = self.findMidPoint(t.A, t.C, z)
                pointList.append(a)
                pointList.append(b)
                self.addPointsInMiddle(pointList, a, b, gridSpace)

            elif t.A.Z == z:
                pointList.append([t.A.X, t.A.Y])

            elif t.B.Z == z:
                pointList.append([t.B.X, t.B.Y])

            elif t.C.Z == z:
                pointList.append([t.C.X, t.C.Y])




        # remove duplicate points in point list...
        templist = []
        while len(pointList) > 0:
            a = pointList[0]
            templist.append(a)
            while(pointList.count(a) > 0):
                pointList.remove(a)
        pointList = templist

        
        printPointList = []
        count = len(pointList)

        # just to have a start point
        point = pointList[0]
        pointList.remove(point)  
        printPointList.append(point)
        lastPoint = point
        print "last point ", point

        count = 0
        n = len(pointList)
        while(count < n):
            point = self.yankNearestN(pointList, lastPoint)
            printPointList.append(point)
            lastPoint = point
            count += 1

        c = canvas.canvas()

        # Start Path Printing
        q = path.path()

        a = printPointList[0]
        q.append( path.moveto(a[0], a[1]) ) 

        count = 1
        n = len(printPointList)
        print "n = ", n
        while(count < n):
            a = printPointList[count]
            q.append(path.lineto( a[0], a[1] )) 
            count += 1

        q.append( path.closepath() ) 

        c.stroke(q, [style.linewidth.THIN])

        #c.stroke(path.circle(1.35, 1.0, 0.1), [style.linewidth.THIN])
        #c.stroke(path.circle(2.35, 1.0, 0.1), [style.linewidth.THIN])

        c.writePDFfile(fileName)


# here try this out

if __name__ == "__main__":

    s = stlObject("Camera.STL")
    #s.printAllTriangles()
    print s.boundingDimensions()




        


