# In the routine below, you should draw your initials in perspective

from matlib import *
from drawlib import *

def persp_initials():
    gtInitialize()
    gtPerspective (60, -100, 100)
    
    gtPushMatrix()
    gtTranslate(0, 0.5, -4)
    gtRotateX(30)
    gtRotateY(30)
    O()
    gtPopMatrix()
    
    #gtPushMatrix()
    #gtTranslate(-1, 0.5, -6)
    #gtTranslate(0, 0, -4)
    #gtScale(0.5, 0.5, 0.5)
    #gtTranslate(-1.25, 1.1, 0)
    #gtRotateX(-20)
    #gtRotateY(-20)
    #O()
    #gtPopMatrix()
    

def F():
    gtBeginShape()
    
    # top
    gtVertex(0, 0, 0.5)
    gtVertex(0, 1, 0.5)
    gtVertex(0, 1, 0.5)
    gtVertex(0.66, 1, 0.5)
    gtVertex(0.66, 1, 0.5)
    gtVertex(0.66, 0.8, 0.5)
    gtVertex(0.66, 0.8, 0.5)
    gtVertex(0.225, 0.8, 0.5)
    gtVertex(0.225, 0.8, 0.5)
    gtVertex(0.225, 0.65, 0.5)
    gtVertex(0.225, 0.65, 0.5)
    gtVertex(0.55, 0.65, 0.5)
    gtVertex(0.55, 0.65, 0.5)
    gtVertex(0.55, 0.45, 0.5)
    gtVertex(0.55, 0.45, 0.5)
    gtVertex(0.225, 0.45, 0.5)
    gtVertex(0.225, 0.45, 0.5)
    gtVertex(0.225, 0, 0.5)
    gtVertex(0.225, 0, 0.5)
    gtVertex(0, 0, 0.5)
    
    # bottom
    gtVertex(0, 0, -0.5)
    gtVertex(0, 1, -0.5)
    gtVertex(0, 1, -0.5)
    gtVertex(0.66, 1, -0.5)
    gtVertex(0.66, 1, -0.5)
    gtVertex(0.66, 0.8, -0.5)
    gtVertex(0.66, 0.8, -0.5)
    gtVertex(0.225, 0.8, -0.5)
    gtVertex(0.225, 0.8, -0.5)
    gtVertex(0.225, 0.65, -0.5)
    gtVertex(0.225, 0.65, -0.5)
    gtVertex(0.55, 0.65, -0.5)
    gtVertex(0.55, 0.65, -0.5)
    gtVertex(0.55, 0.45, -0.5)
    gtVertex(0.55, 0.45, -0.5)
    gtVertex(0.225, 0.45, -0.5)
    gtVertex(0.225, 0.45, -0.5)
    gtVertex(0.225, 0, -0.5)
    gtVertex(0.225, 0, -0.5)
    gtVertex(0, 0, -0.5)
    
    # connect
    gtVertex(0, 0, 0.5)
    gtVertex(0, 0, -0.5)
    gtVertex(0, 1, 0.5)
    gtVertex(0, 1, -0.5)
    gtVertex(0.66, 1, 0.5)
    gtVertex(0.66, 1, -0.5)
    gtVertex(0.66, 0.8, 0.5)
    gtVertex(0.66, 0.8, -0.5)
    gtVertex(0.225, 0.8, 0.5)
    gtVertex(0.225, 0.8, -0.5)
    gtVertex(0.225, 0.65, 0.5)
    gtVertex(0.225, 0.65, -0.5)
    gtVertex(0.55, 0.65, 0.5)
    gtVertex(0.55, 0.65, -0.5)
    gtVertex(0.55, 0.45, 0.5)
    gtVertex(0.55, 0.45, -0.5)
    gtVertex(0.225, 0.45, 0.5)
    gtVertex(0.225, 0.45, -0.5)
    gtVertex(0.225, 0, 0.5)
    gtVertex(0.225, 0, -0.5)
    
    gtEndShape()
    

def O():
    gtPushMatrix()
    gtTranslate(-0.5, 0, 0)
    gtScale(1, 1.1, 1)
    gtScale(0.475, 0.475, 1)
    circle()
    gtPopMatrix()
    gtPushMatrix()
    gtTranslate(-0.5, 0, 0)
    gtScale(1, 1.1, 1)

    gtScale(0.3, 0.3, 1)
    circle()
    gtPopMatrix()
    
    gtPushMatrix()
    gtTranslate(0.1, -0.5, 0)
    F()
    gtPopMatrix()
            
def circle():
    steps = 64
    xold = 1
    yold = 0
    gtBeginShape()
    for i in range(steps+1):
        theta = 2 * 3.1415926535 * i / float(steps)
        x = cos(theta)
        y = sin(theta)
        gtVertex (xold, yold, 0.5)
        gtVertex (x, y, 0.5)
        gtVertex (xold, yold, -0.5)
        gtVertex (x, y, -0.5)
        gtVertex (xold, yold, 0.5)
        gtVertex (xold, yold, -0.5)
        gtVertex (x, y, 0.5)
        gtVertex (x, y, -0.5)
        xold = x
        yold = y
    gtEndShape()