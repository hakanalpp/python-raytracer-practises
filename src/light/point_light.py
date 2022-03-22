
from .light import Light


class PointLight(Light):
    def __init__(self, posX, posY, posZ, r,g,b,intensity) -> None:
        super().__init__(posX, posY, posZ, r,g,b,intensity)