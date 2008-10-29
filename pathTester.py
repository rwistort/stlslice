#! /usr/bin/env python

import string
import os
import sys
import collections
from pyx import *


       

if __name__ == "__main__":


        c = canvas.canvas()

        q = path.path()
        q.append( path.moveto( 0.0, 0.0 ) ) 
        q.append( path.lineto( 1.0, 1.0 ) ) 
        q.append( path.lineto( 0.0, 2.0 ) ) 
        q.append( path.lineto( -1.0, 0.0 ) ) 
        q.append( path.closepath() ) 



        c.stroke(q, [style.linewidth.THIN])
        c.writePDFfile("yes")



