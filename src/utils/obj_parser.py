# CENG 488 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from ..math import HCoord, Point3f, RGBA


def generate_vertices_with_tn(filename):
    with open(filename) as file:
        lines = file.readlines()
        vertices = []
        faces = []
        colors = []
        c = RGBA(0,0,0,0)
        normals = []
        for line in lines:
            line = line.strip()
            if(line.startswith("c ")):
                l = line.split(" ")
                c = RGBA(int(l[1]), int(l[2]), int(l[3]), int(l[4]))
            if(line.startswith("v ")):
                l = line.split(" ")
                vertices.append(Point3f(float(l[1]), float(l[2]), float(l[3])))
            elif(line.startswith("f ")):
                if ("//" in line):
                    m = [int(j.split("//")[0])-1 for j in line.split(" ")[1:]]
                else:
                    m = [int(j.split("/")[0])-1 for j in line.split(" ")[1:]]
                normal1 = HCoord.get_normal_vector(vertices[m[0]], vertices[m[1]], vertices[m[2]])
                normal2 = HCoord.get_normal_vector(vertices[m[0]], vertices[m[2]], vertices[m[3]])
                faces.append([m[0], m[1], m[2]])
                faces.append([m[0], m[2], m[3]])
                normals.append(normal1)
                normals.append(normal2)
                colors.append(c)
                colors.append(c)

    return [vertices, faces, normals, colors]