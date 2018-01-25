# Sample code for starting the mesh processing project
import random

rotate_flag = True    # automatic rotation of model?
time = 0   # keep track of passing time, for automatic rotation

geometryTable = []
faceList = []
colorWhite = False
colorRandom = False
vertexShade= False

# initalize stuff
def setup():
    size (600, 600, OPENGL)
    noStroke()

# draw the current mesh
def draw():
    global time, geometryTable, faceList, colorWhite, vertexShade
    
    background(0)    # clear screen to black

    perspective (PI*0.333, 1.0, 0.01, 1000.0)
    camera (0, 0, 5, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    scale (1, -1, 1)    # change to right-handed coordinate system
    
    # create an ambient light source
    ambientLight (102, 102, 102)
  
    # create two directional light sources
    lightSpecular (204, 204, 204)
    directionalLight (102, 102, 102, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    fill (50, 50, 200)            # set polygon color
    ambient (200, 200, 200)
    specular (0, 0, 0)            # no specular highlights
    shininess (1.0)
  
    rotate (time, 1.0, 0.0, 0.0)

    # THIS IS WHERE YOU SHOULD DRAW THE MESH
    for face in faceList:
        fill(face.r, face.g, face.b)
        vertexIndex = (face.v1, face.v2, face.v3)
        beginShape()
        for index in vertexIndex:
            vert = geometryTable[index]
            if vertexShade == True:
                normal(vert.x, vert.y, vert.z)
            vertex(vert.x, vert.y, vert.z)
        endShape(CLOSE)

    popMatrix()
    
    # maybe step forward in time (for object rotation)
    if rotate_flag:
        time += 0.02

# process key presses
def keyPressed():
    global rotate_flag, colorWhite, faceList, vertexShade
    if key == ' ':
        rotate_flag = not rotate_flag
    elif key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == '5':
        read_mesh ('torus.ply')
    elif key == 'n':
        vertexShade = not vertexShade
    elif key == 'r':
        colorWhite = False
        vertexShade = False
        for face in faceList:
            face.setColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    elif key == 'w':
        vertexShade = False
        colorWhite = not colorWhite
        for face in faceList:
            if colorWhite == True:
                face.setColor(255, 255, 255)
            else:
                face.setColor(200, 200, 200)
    elif key == 'd':
        dual()
    elif key == 'q':
        exit()

# read in a mesh file (THIS NEEDS TO BE MODIFIED !!!)
def read_mesh(filename):
    global geometryTable, faceList

    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
        
    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    geometryTable = []
    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        print "vertex = ", x, y, z
        geometryTable.append(Vertex(x, y, z))
    
    faceList = []
    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if nverts != 3:
            print "error: this face is not a triangle"
            exit()
        
        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        print "face =", index1, index2, index3
        faceList.append(Face(index1, index2, index3))


def dual():
    global geometryTable, faceList
    
    vertexTable = createVertexTable(faceList)
    oppositeTable = createOppositeTable(vertexTable)
    centroidList = getCentroidList(faceList)

    # for each vertex, set their associated faces
    for vertexIndex in range(len(geometryTable)):
        triangles = []
        for c in range(len(vertexTable)):
            if vertexTable[c] == vertexIndex:
                triangles.append(getTriangle(c))
                swinged = swing(c, oppositeTable)
                while swinged != c:
                    triangles.append(getTriangle(swinged))
                    swinged = swing(swinged, oppositeTable)
                break
        geometryTable[vertexIndex].setFaces(triangles)
    
    for vert in geometryTable:
        faces = vert.faces
        weightx = 0
        weighty = 0
        weightz = 0
        for face in faces:
            centroid = centroidList[face]
            weightx += centroid.x
            weighty += centroid.y
            weightz += centroid.z
        weightx /= len(faces)
        weighty /= len(faces)
        weightz /= len(faces)
        vertexCentroid = Vertex(weightx, weighty, weightz)
        vert.setCentroid(vertexCentroid)
        centroidList.append(vertexCentroid)

    newFaces = []
    count = 0
    for vert in geometryTable:
        faces = vert.faces
        for i in range(len(faces)):
            newFaces.append(Face(faces[i], faces[(i+1)%len(faces)], len(faceList)+count))
        count += 1
    
    geometryTable = centroidList
    faceList = newFaces


def getRight(c, oppositeTable):
    return oppositeTable[getNext(c)]


def swing(c, oppositeTable):
    return getNext(getRight(c, oppositeTable))


def getCentroidList(faceList):
    centroidList = []
    for face in faceList:
        vertexIndex = (face.v1, face.v2, face.v3)
        cx = 0
        cy = 0
        cz = 0
        for index in vertexIndex:
            vert = geometryTable[index]
            cx += vert.x
            cy += vert.y
            cz += vert.z
        cx /= 3
        cy /= 3
        cz /= 3
        centroidList.append(Vertex(cx, cy, cz))
    return centroidList

def createVertexTable(facelist):
    vertexTable = []
    for face in faceList:
        vertexTable.append(face.v1)
        vertexTable.append(face.v2)
        vertexTable.append(face.v3)
    return vertexTable

def createOppositeTable(vertexTable):
    oppositeTable = [0 for i in range(len(vertexTable))]
    for a in range(len(vertexTable)):
        for b in range(len(vertexTable)):
            if vertexTable[getNext(a)] == vertexTable[getPrevious(b)] and vertexTable[getPrevious(a)] == vertexTable[getNext(b)]:
                oppositeTable[a] = b
                oppositeTable[b] = a
    return oppositeTable

def getTriangle(c):
    return (int) (c / 3)
    
def getNext(c):
    return (int) (3 * (c/3) + ((c+1) % 3))
    
def getPrevious(c):
    return getNext(getNext(c))
    

class Vertex():
    def __init__(self, X, Y, Z):
        self.x = X
        self.y = Y
        self.z = Z
    
    def setFaces(self, triangles):
        self.faces = triangles

    def setCentroid(self, vert):
        self.centroid = vert
        
class Face():
    def __init__(self, a, b, c):
        self.v1 = a
        self.v2 = b
        self.v3 = c
        self.r = 200
        self.g = 200
        self.b = 200
        
    def setColor(self, R, G, B):
        self.r = R
        self.g = G
        self.b = B