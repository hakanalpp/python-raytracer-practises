from PySide2.QtGui import *


class RGBA:
    def __init__(self, r, g, b, a=1):
        self.r = max(0, min(r, 1))
        self.g = max(0, min(g, 1))
        self.b = max(0, min(b, 1))
        self.a = max(0, min(a, 1))
        self.l = [self.r, self.g, self.b, self.a]

    # def asList(self, faceCount):
    #     return [self.r, self.g, self.b, self.a] * faceCount

    # def to_qcolor(self):
    #     return QColor(self.r, self.g, self.b)

    def __mul__(self, color: "RGBA") -> "RGBA":
        return RGBA(self.r * color.r, self.g * color.g, self.b * color.b)

    def __add__(self, color: "RGBA") -> "RGBA":
        return RGBA(self.r + color.r, self.g + color.g, self.b + color.b)

    def multiply_list(self, color_list: "list[float]"):
        return RGBA(
            self.r * color_list[0], self.g * color_list[1], self.b * color_list[2]
        )

    def scalar_product(self, factor: "float"):
        return RGBA(self.r * factor, self.g * factor, self.b * factor)

    def __str__(self) -> str:
        return f"RGBA: [{self.r}, {self.g}, {self.b}]"