import copy

class Point:
    def __init__(self, x=0, y=0, z=0):
        #assert type(x) in [int, float], type(x)
        self.x = x
        self.y = y
        self.z = z
    
    @classmethod
    def from_Point(cls, pt):
        return cls(pt.x, pt.y, pt.z)
    
    @classmethod
    def from_tuple(cls, tup):
        return cls(tup[0], tup[1], tup[2])
    
    def __add__(self, other):
        #print(type(self), type(other))
        return Point(self.x+other.x, self.y+other.y, self.z+other.z) #, self.d+other.d)
    
    def __str__(self):
        return f"<{self.x}, {self.y}, {self.z}>" #", {self.d}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if type(other) is tuple:
            return self.x == other[0] and self.y == other[1] and self.z == other[2]
        elif other is None:
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z #and self.d == other.d
        
    def __hash__(self):
        return hash(self.tuple()) #, self.d)))
    
    @classmethod
    def new(cls, pt):
        return cls(pt.x, pt.y, pt.z) #, pt.d)
    
    def tuple(self):
        return (self.x, self.y, self.z)
    
    def Rotate(self, direction):
        rotatedCoords = Point(0, 0)
        
        direction = direction & 3
        #print(direction)
        if direction == 3:
            rotatedCoords.x = -self.y;
            rotatedCoords.y = self.x;
            
        elif direction == 0:
            rotatedCoords.x = self.x;
            rotatedCoords.y = self.y;
            
        elif direction == 1:
            rotatedCoords.x = self.y;
            rotatedCoords.y = -self.x;
            
        elif direction == 2:
            rotatedCoords.x = -self.x;
            rotatedCoords.y = -self.y;

        else:
            raise Exception(direction)

        return rotatedCoords

class Vector:
    def __init__(self, pt, dir_=None): #, diag_=None):
        if type(pt) is Vector:
            self.pt = Point.new(pt.pt)
            self.direction = pt.direction
            #self.diag = pt.diag
        else:
            self.pt = pt
            self.direction = dir_
            #self.diag = diag_
    
    @classmethod
    def new(cls, v):
        return cls(Point.new(v.pt), v.direction) #, v.diag)
    
    def __eq__(self, other):
        return self.direction == other.direction and self.pt == other.pt #and self.diag == other.diag
    
    def __hash__(self):
        return hash(tuple((self.pt, self.direction))) #, self.diag)))
    
    def __str__(self):
        return f"{self.pt}, {self.direction}" #", {self.diag}"

COORDS_XY_STEP = 32
CoordsDirectionDelta = [
    Point( -COORDS_XY_STEP, 0 ),
    Point(               0, +COORDS_XY_STEP ),
    Point( +COORDS_XY_STEP, 0 ),
    Point(               0, -COORDS_XY_STEP ),
    Point( -COORDS_XY_STEP, +COORDS_XY_STEP ),
    Point( +COORDS_XY_STEP, +COORDS_XY_STEP ),
    Point( +COORDS_XY_STEP, -COORDS_XY_STEP ),
    Point( -COORDS_XY_STEP, -COORDS_XY_STEP )
]

# adapted from https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/
def Bresenham3D(x1, y1, z1, x2, y2, z2):
    ListOfPoints = []
    ListOfPoints.append((x1, y1, z1))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    if (x2 > x1):
        xs = 1
    else:
        xs = -1
    if (y2 > y1):
        ys = 1
    else:
        ys = -1
    if (z2 > z1):
        zs = 1
    else:
        zs = -1
  
    # Driving axis is X-axis"
    if (dx >= dy and dx >= dz):        
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while (x1 != x2):
            x1 += xs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dx
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            ListOfPoints.append((x1, y1, z1))
  
    # Driving axis is Y-axis"
    elif (dy >= dx and dy >= dz):       
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while (y1 != y2):
            y1 += ys
            if (p1 >= 0):
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            ListOfPoints.append((x1, y1, z1))
  
    # Driving axis is Z-axis"
    else:        
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while (z1 != z2):
            z1 += zs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dz
            if (p2 >= 0):
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            ListOfPoints.append((x1, y1, z1))
    return [Point(x, y, z) for x, y, z in ListOfPoints]
