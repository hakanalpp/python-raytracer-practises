from math import sqrt

from .camera import Camera
from .math.vector import RGBA
from .ray.ray import Ray
from .shape.sphere import Sphere


class Scene:
    def __init__(self, xRes, yRes, camera: 'Camera', objects: 'list[Sphere]', samples) -> 'Scene':
        self.resolution: 'tuple(int, int)'= (xRes, yRes)
        self.camera: 'Camera' = camera
        self.objects: 'list[Sphere]' = objects
        self.samples = samples
        self.sentRayCount = 0

    def send_ray(self, x,y) -> 'RGBA':
        self.sentRayCount += 1

        ray: 'Ray' = self.camera.getRay(x, y)
        return self.trace(ray)

    def trace(self, ray: 'Ray') -> 'RGBA':
        inter = float('inf')
        color = RGBA(0,0,0,0)
        for obj in self.objects:
            tempInt = self.intersect(ray, obj)
            if(tempInt != -1 and tempInt < inter):
                inter = tempInt
                color = obj.color
        return color
    
    def intersect(self, ray: 'Ray', obj: 'Sphere') -> 'float': # TODO
        oc = ray.position - obj.position
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - (obj.radius* obj.radius)
        sqr_disc = b*b - 4*a*c
        if sqr_disc < 0:
            return -1
        discriminant = sqrt(sqr_disc)
        if (a == 0): a = 0.0000000001 # prevent division by zero
        t0 = (-b + discriminant)/(2*a)
        t1 = (-b - discriminant)/(2*a) 
        return min(t0,t1)