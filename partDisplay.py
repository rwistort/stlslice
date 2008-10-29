#! /usr/bin/env python

import string
import os
import sys
import collections
import stlUpload as stl


       

if __name__ == "__main__":

    s = stl.stlModel("Camera_cm.STL")
    #s.printAllTriangles()
    s.findMinAndMazZ()

    # inch
    thickness = 0.15
    initOffset = 0.075
    minHeight = 0.0
    maxHeight = 5.0

    # convert to cm
    thickness *= 2.54
    initOffset *= 2.54
    minHeight *= 2.54
    maxHeight *= 2.54

    baseFileName = "imageFiles/cameraLayer_"

    layer = minHeight + initOffset
    count = 1
    while layer < maxHeight:  
        fileName = baseFileName + str(count)
        #s.computeLayer(layer, 0.10, fileName)    
        layer += thickness
        count += 1


                



