### A simple 3d example for NodeBox by Mark Meyer
### http://www.photo-mark.com
 

from Numeric import *


angle = 180 * (3.1415 / 180)

x = 10
y =  10 
z =  10

#x y z
matrix = array(([x,], [y,], [z,], [1,]), Float)
print matrix 

#y
rot = array(([cos(angle), 0, sin(angle), 0],
              [0, 1, 0, 0],
              [-sin(angle), 0, cos(angle), 0],
              [0, 0, 0, 1]), Float)

matrix = matrixmultiply(rot, matrix)
x = matrix[0] 
y = matrix[1] 
z = matrix[2] 
print x, " ", y, " ", z, " " 


#x
rot = array(([1, 0, 0, 0],
              [0, cos(angle), -sin(angle), 0],
              [0, sin(angle), cos(angle), 0],
              [0, 0, 0, 1]), Float)

#y
rot = array(([cos(angle), 0, sin(angle), 0],
              [0, 1, 0, 0],
              [-sin(angle), 0, cos(angle), 0],
              [0, 0, 0, 1]), Float)

#z
rot = array(([cos(angle),  -sin(angle), 0, 0],
              [sin(angle), cos(angle), 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]), Float)










