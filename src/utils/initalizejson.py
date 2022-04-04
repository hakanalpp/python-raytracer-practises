# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from ..light.point_light import PointLight
from ..shading.lambert_shader import LambertShader
from .obj_parser import generate_vertices_with_tn
from ..camera import Camera
from ..scene import Scene
from ..shape import Sphere, Mesh, Material
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

    materials = []
    for m in obj["materials"]:
        materials.append(
            Material(
                m["name"],
                m["reflection"],
                m["refraction"],
            )
        )

    default_material = Material("default", 0, 0)
    material_names = list(map(lambda x: x.name, materials))

    lambert_shader = LambertShader(lights)
    for o in obj["meshes"]:
        specs = generate_vertices_with_tn(o["filename"])
        shader = None
        if o["shader_type"] == "Lambert":
            shader = lambert_shader
        t = "default"
        if "obj_type" in o:
            t = o["obj_type"]

        material = default_material
        if "material" in o and o["material"] in material_names:
            material = materials[material_names.index(o["material"])]

        objects.append(Mesh(specs[0], specs[1], specs[2], specs[3], material, shader, t))

    return Scene(
        settings["xres"],
        settings["yres"],
        camera,
        objects,
        lights,
        settings["worker_count"],
        settings["bounce_count"],
    )
