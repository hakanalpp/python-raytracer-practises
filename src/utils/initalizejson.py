# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from ..light.point_light import PointLight
from ..shading.lambert_shader import LambertShader
from .obj_parser import generate_vertices_with_tn
from ..camera import Camera
from ..scene import Scene
from ..shape import Sphere, Mesh
from .readjson import readJson


def initalize_scene(filename) -> "Scene":
    obj = readJson(filename)
    settings = obj["renderSettings"]
    cam = obj["camera"]

    camera = Camera(
        cam["posX"],
        cam["posY"],
        cam["posZ"],
        cam["fov"],
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

    objects = []
    for s in obj["spheres"]:
        objects.append(
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

    for o in obj["meshes"]:
        specs = generate_vertices_with_tn(o["filename"])
        objects.append(Mesh(specs[0], specs[1], specs[2], specs[3]))

    lights = []
    for l in obj["lights"]:
        if l["type"] == "PointLight":
            lights.append(
                PointLight(
                    l["posX"],
                    l["posY"],
                    l["posZ"],
                    l["color"]["r"],
                    l["color"]["g"],
                    l["color"]["b"],
                    l["intensity"],
                )
            )

    shader = None
    if settings["shader_type"] == "Lambert":
        shader = LambertShader(lights)

    return Scene(
        settings["xres"], settings["yres"], camera, objects, settings["samples"], shader
    )
