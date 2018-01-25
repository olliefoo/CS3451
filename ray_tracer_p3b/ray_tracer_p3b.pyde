# This is the starter code for the CS 3451 Ray Tracing project.
#
# The most important part of this code is the interpreter, which will
# help you parse the scene description (.cli) files.

import math

# used to store scene properties and lists of objects, lights, surfaces
class Stats():
    def __init__(self):
        self.fov = 0
        self.BGr = 0
        self.BGg = 0 
        self.BGb = 0 
        self.lightList = []
        self.shapeList = []
        
        
class Surface():
    def __init__(self, d1, d2, d3, a1, a2, a3, s1, s2, s3, phong, refl):
        self.Cdr = d1 
        self.Cdg = d2 
        self.Cdb = d3
        self.Car = a1
        self.Cag = a2
        self.Cab = a3
        self.Csr = s1
        self.Csg = s2
        self.Csb = s3
        self.P = phong
        self.Krefl = refl


class Light():
    def __init__(self, x, y, z, R, G, B):
        self.position = (x, y, z)
        self.r = R
        self.g = G
        self.b = B

        
        
        
class Ray():
    # o, d are tuples : (x, y, z)
    def __init__(self, o, d):
        self.origin = o
        self.direction = d
        
    def getPoint(self, t):
        o = self.origin
        d = self.direction
        return (o[0] + t*d[0], o[1] + t*d[1], o[2] + t*d[2])


class Sphere():
    def __init__(self, r, x, y, z, surf):
        self.center = (x, y, z)
        self.radius = r
        self.surface = surf
    
    # returns the normal given a vertex on the sphere (already normalized)
    def getNormal(self, intersection):
        ix, iy, iz = intersection
        cx, cy, cz = self.center
        N = PVector(ix-cx, iy-cy, iz-cz)  
        N.normalize()
        return N
    
    # returns the ray-sphere intersect point, or None
    def intersect(self, ray):
        dx, dy, dz = ray.direction
        x0, y0, z0 = ray.origin
        cx, cy, cz = self.center
        r = self.radius
        
        a = dx**2 + dy**2 + dz**2
        b = 2 * ((x0*dx - cx*dx) + (y0*dy - cy*dy) + (z0*dz - cz*dz))
        c = (x0-cx)**2 + (y0-cy)**2 + (z0-cz)**2 - r**2
        discriminant = (b*b) - (4*a*c)
        
        # imaginary roots = no intersection
        t = 0
        if discriminant < 0:
            return None
        elif discriminant == 0:
            t = -b / (2*a)
            if t < 0:
                return None
        else:
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            # picks the smallest t value
            t = min(root1, root2)
            if t < 0:
                return None
            
        return ray.getPoint(t)

class Triangle():
    def __init__(self, a, b, c, surf):
        self.v1 = b
        self.v2 = a
        self.v3 = c
        self.surface = surf
        
        # plane calculations
        x1, y1, z1 = self.v1
        x2, y2, z2 = self.v2
        x3, y3, z3 = self.v3
        vec1 = PVector(x2-x1, y2-y1, z2-z1)
        vec2 = PVector(x3-x1, y3-y1, z3-z1)
        # finds the normal vector. N = (a, b, c)
        n = vec1.cross(vec2)
        n.normalize()
        
        self.N = n
        self.d = - n.dot(PVector(x1, y1, z1))
    
    # returns the normal (already normalized)
    def getNormal(self, intersection):
        return self.N
        
    # return ray-triangle intersect point, or None
    def intersect(self, ray):
        dx, dy, dz = ray.direction
        x0, y0, z0 = ray.origin
        origin = PVector(x0, y0, z0)
        direction = PVector(dx, dy, dz)
        
        x1, y1, z1 = self.v1
        x2, y2, z2 = self.v2
        x3, y3, z3 = self.v3
        N = self.N
        d = self.d
        
        # if the ray and plane are orthogonal, no intersect
        bottom = N.dot(direction)
        if bottom == 0:
            return None
        
        top = N.dot(origin)
        t = - (top + d) / bottom
        if t < 0:
            return None
        
        intersection = ray.getPoint(t)
        # now have to check if the intersection is inside the triangle
        x, y, z = intersection
        
        e1 = PVector(x2-x1, y2-y1, z2-z1)
        p1 = PVector(x-x1, y-y1, z-z1)
        test1 = e1.cross(p1)
        if N.dot(test1) < 0:
            return None
        
        e2 = PVector(x3-x2, y3-y2, z3-z2)
        p2 = PVector(x-x2, y-y2, z-z2)
        test2 = e2.cross(p2)
        if N.dot(test2) < 0:
            return None
        
        e3 = PVector(x1-x3, y1-y3, z1-z3)
        p3 = PVector(x-x3, y-y3, z-z3)
        test3 = e3.cross(p3)
        if N.dot(test3) < 0:
            return None
        
        return intersection
        

def setup():
    size(500, 500) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)


# read and interpret the appropriate scene description .cli file based on key press
def keyPressed():
    if key == '1':
        interpreter("i1.cli")
    elif key == '2':
        interpreter("i2.cli")
    elif key == '3':
        interpreter("i3.cli")
    elif key == '4':
        interpreter("i4.cli")
    elif key == '5':
        interpreter("i5.cli")
    elif key == '6':
        interpreter("i6.cli")
    elif key == '7':
        interpreter("i7.cli")
    elif key == '8':
        interpreter("i8.cli")
    elif key == '9':
        interpreter("i9.cli")
    elif key == '0':
        interpreter("i10.cli")


def interpreter(fname):
    # instantiate a stats object that stores all necessary information from the file
    stats = Stats()
    
    # used to store the vertices of the triangle
    v1 = None
    v2 = None
    v3 = None
    
    # used to store the surface info
    surface = None
    
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # parse each line in the file in turn
    for line in lines:
        words = line.split()  # split the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            stats.shapeList.append(Sphere(float(words[1]), float(words[2]), float(words[3]), \
                                          float(words[4]), surface))
        elif words[0] == 'fov':
            # makes sure fov is in radians
            stats.fov = math.radians(float(words[1]))
        elif words[0] == 'background':
            stats.BGr = float(words[1])
            stats.BGg = float(words[2])
            stats.BGb = float(words[3])
        elif words[0] == 'light':
            stats.lightList.append(Light(float(words[1]), float(words[2]), float(words[3]), \
                                         float(words[4]), float(words[5]), float(words[6])))
        elif words[0] == 'surface':
            surface = Surface(float(words[1]), float(words[2]), float(words[3]), \
                              float(words[4]), float(words[5]), float(words[6]), \
                              float(words[7]), float(words[8]), float(words[9]), \
                              float(words[10]), float(words[11]))
        elif words[0] == 'begin':
            v1 = None
            v2 = None
            v3 = None
        elif words[0] == 'vertex':
            if v1 == None:
                v1 = (float(words[1]), float(words[2]), float(words[3]))
            elif v2 == None:
                v2 = (float(words[1]), float(words[2]), float(words[3]))
            else:
                v3 = (float(words[1]), float(words[2]), float(words[3]))
        elif words[0] == 'end':
            stats.shapeList.append(Triangle(v1, v2, v3, surface))
        elif words[0] == 'write':
            render_scene(stats)    # render the scene
            save(words[1])  # write the image to a file
            pass


# render the ray tracing scene
def render_scene(stats):
                    
    k = math.tan(stats.fov/2)
    z = -1
    
    for y in range(height):
        for x in range(width):
            # create an eye ray for pixel (x,y) and cast it into the scene        
            # perspective projection from 2D to 3D
            x1 = x / abs(z)
            y1 = (height-y) / abs(z)
            x2 = (x1 - (width/2)) * ((2*k) / width)
            y2 = (y1 - (height/2)) * ((2*k) / height)
            
            # ray origin is at 0, 0, 0
            ray = Ray((0, 0, 0), (x2, y2, z))
            
            closest = None
            intersection = None
            
            # for each shape, find the closest intersection point
            for object in stats.shapeList:
                
                v = object.intersect(ray)
                                
                # finds the closest intersection from all the objects
                if not intersection == None and not v == None:
                    oldDistance = dist(0, 0, 0, intersection[0], intersection[1], intersection[2])
                    newDistance = dist(0, 0, 0, v[0], v[1], v[2])
                
                if not v == None and (intersection == None or (newDistance < oldDistance)):
                    intersection = v
                    closest = object
          
            # color calculation
            
            # if ray misses all objects, then color pixel with background color
            if closest == None:
                pix_color = color(stats.BGr, stats.BGg, stats.BGb)
            else:
                r, g, b = calculateColor(stats, closest, intersection, 0)
                pix_color = color(r, g, b)
            
            # fill the pixel with the calculated color
            set (x, y, pix_color)         


# used to calculate the color of a pixel
def calculateColor(stats, object, intersection, depth):
    ix, iy, iz = intersection

    # retrieves the already normalized normal vector
    N = object.getNormal(intersection)
                
    surface = object.surface
    diffuse = (surface.Cdr, surface.Cdg, surface.Cdb)
    amb = (surface.Car, surface.Cag, surface.Cab)
    spec = (surface.Csr, surface.Csg, surface.Csb)
    phong = surface.P
    reflect = surface.Krefl
    
    # color (r,g,b) sum to be added to
    sum = [0, 0, 0]
    
    # caluclates the vector from the point to eye. Used for reflection and specular
    V = PVector(-ix, -iy, -iz)
    V.normalize()
    
    # reflection calculation
    if depth < 12 and reflect > 0:
        R = PVector.mult(N, 2 * N.dot(V))
        R = PVector.sub(R, V)
        R.normalize()
        
        # used to push ray origin out of object
        Err = PVector.mult(N, 1e-12)
        reflectRay = Ray((ix+Err.x, iy+Err.y, iz+Err.z), (R.x, R.y, R.z))
        
        closest = None
        hitPoint = None
        for obj in stats.shapeList:
            if obj is not object:
                v = obj.intersect(reflectRay)
                # finds the closest reflect ray intersection from the current intersection
                if not hitPoint == None and not v == None:
                    oldDistance = dist(ix, iy, iz, hitPoint[0], hitPoint[1], hitPoint[2])
                    newDistance = dist(ix, iy, iz, v[0], v[1], v[2])
                if not v == None and (hitPoint == None or (newDistance < oldDistance)):
                    hitPoint = v
                    closest = obj
        if closest == None:
            BGcolor = (stats.BGr, stats.BGg, stats.BGb)
            for i in range(0, 3):
                sum[i] += (reflect * BGcolor[i])
        else:
            reflectColor = calculateColor(stats, closest, hitPoint, depth+1)    
            for i in range(0, 3):
                sum[i] += (reflect * reflectColor[i])
            
            
    # ambient shading
    for i in range(0, 3):
        sum[i] += amb[i]
        
    for light in stats.lightList:
        lx, ly, lz = light.position
        light_color = (light.r, light.g, light.b)
        
        shadow = False
        # creates a ray from the point to the light source
        lightRay = Ray((ix, iy, iz), (lx-ix, ly-iy, lz-iz))
        for obj in stats.shapeList:
            if obj is not object:
                v = obj.intersect(lightRay)
                if not v == None:
                    lightDistance = dist(ix, iy, iz, lx, ly, lz)
                    intersectDistance = dist(ix, iy, iz, v[0], v[1], v[2])
                    if intersectDistance < lightDistance:
                        shadow = True
        
        # if point is in shadow, light color does not contribute
        if shadow == True:
            light_color = (0, 0, 0)        
    
        L = PVector(lx-ix, ly-iy, lz-iz)
        L.normalize()
                
        # for specular shading
        #V = PVector(-ix, -iy, -iz)
        #V.normalize()
        H = PVector.add(L, V)
        H.normalize()
                                
        for i in range(0, 3):
            sum[i] += (diffuse[i] * light_color[i] * max(0, N.dot(L))) + (spec[i] * light_color[i] * max(0, N.dot(H))**phong)
        
    # makes sure sum can't add up to more than 255
    for i in range(0, 3):
        if sum[i] > 1:
            sum[i] = 1
                
    r, g, b = sum
    return (r, g, b)
    
    
# should remain empty for this assignment
def draw():
    pass