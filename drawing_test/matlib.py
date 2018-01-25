# Matrix Stack Library -- Use your code from Project 1A

class Stack:
    matrix = []
        
        
def multiply(a, b):
    result = [[0 for i in range(len(a))] for j in range(len(b))]
    for i in range(len(a)):
        for j in range(len(a[i])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
                
    return result

def multiplyVector(m, v):
    result = [0 for i in range(len(v))]
    for i in range(len(m)):
        for j in range(len(v)):
            result[i] += m[i][j] * v[j]
            
    return result
    
def gtInitialize():
    Stack.matrix = []
    Stack.matrix.append([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])


def gtPushMatrix():
    duplicate = Stack.matrix[-1]
    Stack.matrix.append(duplicate)


def gtPopMatrix():
    if len(Stack.matrix) == 1:
        print 'cannot pop the matrix stack'
    else:
        Stack.matrix.pop()


def gtTranslate(x, y, z):
    oldctm = Stack.matrix[-1]
    transform = [[1,0,0,x], [0,1,0,y], [0,0,1,z], [0,0,0,1]]
    Stack.matrix[-1] = multiply(oldctm, transform)


def gtScale(x, y, z):
    oldctm = Stack.matrix[-1]
    transform = [[x,0,0,0], [0,y,0,0], [0,0,z,0], [0,0,0,1]]
    Stack.matrix[-1] = multiply(oldctm, transform)


def gtRotateX(theta):
    theta = theta*PI/180
    oldctm = Stack.matrix[-1]
    transform = [[1,0,0,0], [0,cos(theta),-sin(theta),0], [0,sin(theta),cos(theta),0], [0,0,0,1]]
    Stack.matrix[-1] = multiply(oldctm, transform)


def gtRotateY(theta):
    theta = theta*PI/180
    oldctm = Stack.matrix[-1]
    transform = [[cos(theta),0,sin(theta),0], [0,1,0,0], [-sin(theta),0,cos(theta),0], [0,0,0,1]]
    Stack.matrix[-1] = multiply(oldctm, transform)


def gtRotateZ(theta):
    theta = theta*PI/180
    oldctm = Stack.matrix[-1]
    transform = [[cos(theta), -sin(theta),0,0], [sin(theta),cos(theta),0,0], [0,0,1,0], [0,0,0,1]]
    Stack.matrix[-1] = multiply(oldctm, transform)