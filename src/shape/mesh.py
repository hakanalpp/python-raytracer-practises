# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from math import inf

from ..shading.shader import Shader
from ..math import RGBA, HCoord, Point3f, Vector3f, Ray
from .shape import Shape
from .material import Material


class Mesh(Shape):
    def __init__(
        self,
        vertices: "list[Point3f]",
        faces: "list[list[int]]",
        normals: "list[Vector3f]",
        colors: "list[RGBA]",
        material: "Material",
        shader: "Shader",
        type: str = "default",
    ) -> "Mesh":
        super(Mesh, self).__init__(material, shader, type)
        self.vertices: "list[Point3f]" = vertices
        self.faces: "list[list[int]]" = faces
        self.normals: "list[Vector3f]" = normals
        self.colors: "list[RGBA]" = colors
        self.calculate_bounding_box()

    def intersect(
        self, ray: "Ray"
    ):  # One ray can not hit two face in one mesh (as you thought), performance improve here later.
        distance = float("inf")
        index = 0
        selected_index = 0
        selected_P = Point3f(-1, -1, -1)
        for f in self.faces:
            temp_d, P = self.intersect_with_face(ray, f, self.normals[index])
            if temp_d != -1 and temp_d < distance:
                distance = temp_d
                selected_index = index
                selected_P = P
            index += 1
        f = self.faces[selected_index]
        v = self.vertices
        return [
            distance,
            self.colors[selected_index],
            HCoord.get_normal_vector(v[f[0]], v[f[1]], v[f[2]]),
            selected_P,
        ]

    def intersect_with_face(self, ray: "Ray", face: "list[int]", normal: "Vector3f"):
        nDotRayDirection = normal.dot(ray.direction)
        if (
            abs(nDotRayDirection) < 10e-12 or nDotRayDirection > 0.0
        ):  # Parallel or almost parallel or negative way
            return [-1, -1]
        v = self.vertices

        d = -normal.dot(v[face[0]])
        t = -(normal.dot(ray.position) + d) / nDotRayDirection
        if t <= 0:
            return [-1, -1]  # Triangle is behind

        P = ray.position + t * ray.direction

        edge0 = v[face[1]] - v[face[0]]
        vp0 = P - v[face[0]]
        C = edge0.crossProduct(vp0)
        if normal.dot(C) < 0:
            return [-1, -1]  # P is on the wrong side

        edge1 = v[face[2]] - v[face[1]]
        vp1 = P - v[face[1]]
        C = edge1.crossProduct(vp1)
        if normal.dot(C) < 0:
            return [-1, -1]  # P is on the wrong side

        edge2 = v[face[0]] - v[face[2]]
        vp2 = P - v[face[2]]
        C = edge2.crossProduct(vp2)
        if normal.dot(C) < 0:
            return [-1, -1]  # P is on the wrong side

        return [HCoord.get_length_between_points(ray.position, P), P]

    def calculate_bounding_box(self):
        self.bounding_box.min = Point3f(inf, inf, inf)
        self.bounding_box.max = Point3f(-inf, -inf, -inf)

        for face in self.faces:
            for p in face:
                v = self.vertices[p]
                if v.x > self.bounding_box.max.x:
                    self.bounding_box.max.x = v.x
                if v.y > self.bounding_box.max.y:
                    self.bounding_box.max.y = v.y
                if v.z > self.bounding_box.max.z:
                    self.bounding_box.max.z = v.z

                if v.x < self.bounding_box.min.x:
                    self.bounding_box.min.x = v.x
                if v.y < self.bounding_box.min.y:
                    self.bounding_box.min.y = v.y
                if v.z < self.bounding_box.min.z:
                    self.bounding_box.min.z = v.z
