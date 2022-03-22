# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from ..ray.ray import Ray
from ..math.vector import RGBA, HCoord, Point3f, Vector3f
from .shape import Shape


class Mesh(Shape):
    def __init__(self, vertices: 'list[Point3f]', faces: 'list[list[int]]', normals: 'list[Vector3f]', colors: 'list[RGBA]') -> "Mesh":
        self.vertices: 'list[Point3f]' = vertices
        self.faces: 'list[list[int]]' = faces
        self.normals: 'list[Vector3f]' = normals
        self.colors: 'list[RGBA]' = colors


    def intersect(self, ray: 'Ray'): # One ray can not hit two face in one mesh (as you thought), performance improve here later. 
        distance = float("inf")
        index = 0
        selected_index = 0
        for f in self.faces:
            temp_d = self.intersect_with_face(ray, f, self.normals[index])
            if(temp_d != -1 and temp_d < distance):
                distance = temp_d
                selected_index = index
            index += 1
        return [distance, self.colors[selected_index]]

    def intersect_with_face(self, ray: 'Ray', face: 'list[int]', normal: 'Vector3f'):
        nDotRayDirection = normal.dot(ray.direction)
        if(abs(nDotRayDirection) < 0.0000001): # Parallel or almost parallel
            return -1
        v = self.vertices

        d = -normal.dot(v[face[0]])
        t = -(normal.dot(ray.position) + d) / nDotRayDirection
        if (t < 0): return -1 # Triangle is behind

        P = ray.position + t * ray.direction

        edge0 = v[face[1]] - v[face[0]]
        vp0 = P - v[face[0]]
        C = edge0.crossProduct(vp0)
        if (normal.dot(C) < 0): return -1 # P is on the wrong side

        edge1 = v[face[2]] - v[face[1]]
        vp1 = P - v[face[1]]
        C = edge1.crossProduct(vp1)
        if (normal.dot(C) < 0): return -1 # P is on the wrong side

        edge2 = v[face[0]] - v[face[2]]
        vp2 = P - v[face[2]]
        C = edge2.crossProduct(vp2)
        if (normal.dot(C) < 0): return -1 # P is on the wrong side

        return HCoord.get_length_between_points(ray.position, P)