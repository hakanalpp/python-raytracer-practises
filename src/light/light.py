
from ..math.vector import RGBA, Point3f


class Light:
    def __init__(self, posX, posY, posZ, r,g,b,intensity) -> None:
        self.position = Point3f(posX, posY, posZ)
        self.color = RGBA(r,g,b,255)
        self.intensity = intensity