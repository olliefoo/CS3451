# Author: Ollie Foo
# gtID: 903071442

array = [[] for i in range(12)]
for i in range(0,12):
    for j in range(2**(i)):
        array[i].append(0)


def setup():
    size(600, 600)
    
        
def convert(x):
    return (x + 3) * 100


def draw():
    background(0, 0, 0)
    noStroke()
    
    x = (mouseX-300) / 100.0
    # y = -(mouseY-300) / 100.0
    y = (mouseY-300) / 100.0
    
    fill(255, 255, 255)
    text(x, 0, 10)
    text(y, 50, 10)
    
    # makes sure that the mouse only registers between -2 and 2
    if x > 2:
        x = 2
    elif x < -2:
        x = -2
    elif y > 2:
        y = 2
    elif y < -2:
        y = -2
                
    v = x + y*1j
    
    fill(0, 128, 256)
    ellipse(width/2, height/2, 4, 4)
    
    for i in range(1, 12):
        
        for j in range(0, 2**i/2):
            z = array[i-1][j] + v**(i-1)
            array[i][j] = z
            fill(3*z.real*128, 128+3*z.imag*64,256-3*(z.real+z.imag)*128)
            ellipse(convert(z.real), convert(z.imag), 4, 4)
            
        for j in range(0, 2**i/2):
            z = array[i-1][j] - v**(i-1)
            array[i][j+2**i/2] = z
            fill(3*z.real*128, 128+3*z.imag*64,256-3*(z.real+z.imag)*128)
            ellipse(convert(z.real), convert(z.imag), 4, 4)

    

    
    

    