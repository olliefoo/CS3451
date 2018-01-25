# Drawing Routines, like OpenGL

from matlib import *


start = False
point = []

class Projection:
    #  0 for no projection, 1 for ortho, 2 for perspective
    mode = 0
    left = 0
    right = 0
    bottom = 0
    top = 0
    near = 0
    far = 0
    fov = 0

def gtOrtho(left, right, bottom, top, near, far):
    Projection.mode = 1
    Projection.left = left
    Projection.right = right
    Projection.bottom = bottom
    Projection.top = top
    Projection.near = near
    Projection.far = far

def gtPerspective(fov, near, far):
    Projection.mode = 2
    Projection.near = near
    Projection.far = far
    Projection.fov = fov

def gtBeginShape():
    global start
    if not start:
        start = True

def gtEndShape():
    global start
    if start:
        start = False

def gtVertex(x, y, z):
    global start
    if start:
        if not point:
            point.append((x,y,z, 1))
        else:
            start = point.pop()
            end = (x,y,z, 1)
            ctm = Stack.matrix[-1]
            start = multiplyVector(ctm, start)
            end = multiplyVector(ctm, end)
                    
            # Orthographic projection
            if Projection.mode == 1:
                start[0] = (width / (Projection.right - Projection.left)) * (start[0] - Projection.left)
                start[1] = (height / (Projection.bottom - Projection.top)) * (start[1] - Projection.top)
                end[0] = (width / (Projection.right - Projection.left)) * (end[0] - Projection.left)
                end[1] = (height / (Projection.bottom - Projection.top)) * (end[1] - Projection.top)
                
            # Perspective projection
            elif Projection.mode == 2:
                sx1 = start[0] / abs(start[2])
                sy1 = start[1] / -abs(start[2])
                ex1 = end[0] / abs(end[2])
                ey1 = end[1] / -abs(end[2])
                
                fov = Projection.fov * PI / 180
                k = tan(fov / 2)
                
                sx2 = (sx1 + k) * (width / (2 * k))
                sy2 = (sy1 + k) * (height / (2 * k))
                ex2 = (ex1 + k) * (width / (2 * k))
                ey2 = (ey1 + k) * (height / (2 * k))
                
                start[0] = sx2
                start[1] = sy2
                end[0] = ex2
                end[1] = ey2

            line(start[0], start[1], end[0], end[1])