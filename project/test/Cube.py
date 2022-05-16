import gmsh
import sys
import os
import numpy as np
import math

class Point(object):
    def __init__(self, tag, x, y, z):
        self.tag = tag
        self.X = x
        self.Y = y
        self.Z = z

    def get_tag(self):
        return self.tag
        
    def get_coords(self):
        return [self.X, self.Y, self.Z]

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getZ(self):
        return self.Z

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        dz = self.Z - other.Z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def move(self, dx, dy, dz):
        self.X = self.X + dx
        self.Y = self.Y + dy
        self.Z = self.Z + dz

    def __str__(self):
        str1 = "Point " + str(self.tag) + " has coords: " + str(self.X) + ", " + str(self.Y) + ", " + str(self.Z) + "\n"
        return str1

class Tetrahedra:
    def __init__(self, tag, nodes_list):
        self.tag = tag
        self.nodes_list = nodes_list

        self.vertex_1 = points[int(nodes_list[0]) - 1]
        self.vertex_2 = points[int(nodes_list[1]) - 1]
        self.vertex_3 = points[int(nodes_list[2]) - 1]
        self.vertex_4 = points[int(nodes_list[3]) - 1]

        self.nodes_coords = Point.get_coords(self.vertex_1) + Point.get_coords(self.vertex_2) + Point.get_coords(self.vertex_3) + Point.get_coords(self.vertex_4)
        self.center = (list(map(lambda x, y, z, v: (x + y + z + v)/4, Point.get_coords(self.vertex_1), 
                                                                    Point.get_coords(self.vertex_2), 
                                                                    Point.get_coords(self.vertex_3),
                                                                    Point.get_coords(self.vertex_4))))

    def add_neighbours(self):
        neighb = []
        for t in triangles:
            nodes = Tetrahedra.get_nodes(t)
            k = 0
            for i in nodes:
                if i in self.nodes_list:
                    k = k+1
            
            if (k == 3):
                neighb.append(Tetrahedra.get_tag(t))

        self.neighbours = tuple(neighb)

    def get_nodes(self):
        return self.nodes_list

    def get_tag(self):
        return self.tag

    def get_neighbours(self):
        return self.neighbours

    def __str__(self):
        nodeCoords_1 =Point.get_coords(self.vertex_1)
        nodeCoords_2 = Point.get_coords(self.vertex_2)
        nodeCoords_3 = Point.get_coords(self.vertex_3)
        nodeCoords_4 = Point.get_coords(self.vertex_4)
        str1 = "Triangle " + str(self.tag) + " has nodes: " + str(self.nodes_list[0]) + ", " + str(self.nodes_list[1]) + ", " + str(self.nodes_list[2]) + ", " + str(self.nodes_list[3]) + "\n"
        str2 = "Nodes coords are:" + "\n" + str(nodeCoords_1) + "\n" + str(nodeCoords_2) +"\n" + str(nodeCoords_3) + "\n" + str(nodeCoords_4) + "\n"
        str3 = "Center coords are: " + str(self.center) + "\n"
        str4 = "Neighbours of this triangle are: " + str(self.neighbours) + "\n"
        return str1 +  str2 + str3 + str4  + "\n"

gmsh.initialize()

path = os.path.dirname(os.path.abspath(__file__))
gmsh.initialize()

gmsh.model.add("Cube")

# Build a cube:
lc = 1
p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(1, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(1, 0, 1, lc)
p4 = gmsh.model.geo.addPoint(0, 0, 1, lc)
p5 = gmsh.model.geo.addPoint(0, 1, 0, lc)
p6 = gmsh.model.geo.addPoint(1, 1, 0, lc)
p7 = gmsh.model.geo.addPoint(1, 1, 1, lc)
p8 = gmsh.model.geo.addPoint(0, 1, 1, lc)

l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)

l5 = gmsh.model.geo.addLine(p5, p6)
l6 = gmsh.model.geo.addLine(p6, p7)
l7 = gmsh.model.geo.addLine(p7, p8)
l8 = gmsh.model.geo.addLine(p8, p5)

l9 = gmsh.model.geo.addLine(p1, p5)
l10 = gmsh.model.geo.addLine(p2, p6)
l11 = gmsh.model.geo.addLine(p3, p7)
l12 = gmsh.model.geo.addLine(p4, p8)

cl1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
cl2 = gmsh.model.geo.addCurveLoop([l5, l6, l7, l8])
cl3 = gmsh.model.geo.addCurveLoop([l9, l5, -l10, -l1])
cl4 = gmsh.model.geo.addCurveLoop([l10, l6, -l11, -l2])
cl5 = gmsh.model.geo.addCurveLoop([l11, l7, -l12, -l3])
cl6 = gmsh.model.geo.addCurveLoop([l12, l8, -l9, -l4])

pl1 = gmsh.model.geo.addPlaneSurface([cl1])
pl2 = gmsh.model.geo.addPlaneSurface([cl2])
pl3 = gmsh.model.geo.addPlaneSurface([cl3])
pl4 = gmsh.model.geo.addPlaneSurface([cl4])
pl5 = gmsh.model.geo.addPlaneSurface([cl5])
pl6 = gmsh.model.geo.addPlaneSurface([cl6])

l = gmsh.model.geo.addSurfaceLoop([i + 1 for i in range(6)])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

# Generate mesh:
gmsh.model.mesh.generate(3)
gmsh.option.setNumber("Mesh.Format", 1)
gmsh.option.setNumber("Mesh.NodeLabels", 1)

# Save mesh:
# gmsh.write(os.path.join(path, os.curdir, "Simple_Cube.msh"))
# gmsh.write(os.path.join(path, os.curdir, "Simple_Cube.geo_unrolled"))

# Access mesh data:
elementTags, elementNodeTags = gmsh.model.mesh.getElementsByType(4)
elemNodeTags = np.array(elementNodeTags) 
NodeTags = np.unique(elemNodeTags) 

N_tetr = len(elementTags)
N_nodes = len(NodeTags)

print("elemTags ", elementTags)
print("elementNodeTags", elementNodeTags)

# Print data about every triangle:
print("Model has", N_tetr, "tetrahedra")
print("Model has", N_nodes, "points")
print("Number of the first tetrahedra:", elementTags[0])

points = []
for i in range(1, N_nodes+1):
    nodeCoords = gmsh.model.mesh.getNode(i)[0]
    p = Point(NodeTags[i-1], nodeCoords[0], nodeCoords[1], nodeCoords[2])
    points.append(p)

triangles = []
for i in range(N_tetr):
    p_tetr = int(i)
    p_nodes = 4*p_tetr
    
    tag = elementTags[p_tetr]                                                       
    nodes_list = (elementNodeTags[p_nodes], elementNodeTags[p_nodes+1], elementNodeTags[p_nodes+2],  elementNodeTags[p_nodes+3]) # кортеж, тк должен быть неизменяемым

    t = Tetrahedra(tag, nodes_list)
    triangles.append(t)


with open(os.path.join(path, os.curdir, "out_3D.txt"), "w") as file:
    for t in triangles:
        Tetrahedra.add_neighbours(t)
        file.write(Tetrahedra.__str__(t))

if "-nopopup" not in sys.argv:
    gmsh.fltk.initialize()
    while gmsh.fltk.isAvailable():
        gmsh.fltk.wait()

# We can use this to clear all the model data:
gmsh.clear()

gmsh.finalize()
