
from abc import abstractmethod

from ..light.light import Light


class Shader:
    def __init__(self, lights) -> None:
        self.lights: 'list[Light]' = lights
        pass

    @abstractmethod
    def calculate_light(self):
        return