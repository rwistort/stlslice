#!/usr/bin/env python


from pyx import *

c = canvas.canvas()

circle = path.circle(0, 0, 0.1)
c.stroke(circle)
circle = path.circle(1, 0, 0.1)
c.stroke(circle)
circle = path.circle(0, 2, 0.1)
c.stroke(circle)
circle = path.circle(-1, 0, 0.1)
c.stroke(circle)



c.writeEPSfile("testEps")
c.writePDFfile("testEps")

