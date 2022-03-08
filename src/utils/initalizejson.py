# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from ..camera import Camera
from ..scene import Scene
from ..shape.sphere import Sphere
from ..utils.readjson import readJson


def initalize_scene(filename) -> "Scene":
    obj = readJson(filename)
    settings = obj["renderSettings"]
    cam = obj["camera"]

    camera = Camera(
        cam["posX"],
        cam["posY"],
        cam["posZ"],
        60,
        cam["focalLength"],
        cam["dirX"],
        cam["dirY"],
        cam["dirZ"],
        cam["upX"],
        cam["upY"],
        cam["upZ"],
        settings["xres"],
        settings["yres"],
    )

    spheres = []
    for s in obj["spheres"]:
        spheres.append(
            Sphere(
                s["posX"],
                s["posY"],
                s["posZ"],
                s["radius"],
                s["color"]["r"],
                s["color"]["g"],
                s["color"]["b"],
            )
        )

    return Scene(
        settings["xres"], settings["yres"], camera, spheres, settings["samples"]
    )
