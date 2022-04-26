# CENG 488 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from ..math import RGBA, Vector3f
from ..accelerator import ListAccelerator, BVHAccelerator
from ..light.point_light import PointLight
from ..shading.lambert_shader import LambertShader
from .obj_parser import generate_vertices_with_tn
from ..camera import Camera
from ..scene import Scene
from ..shape import Sphere, Mesh, Material, AABB, SphereGenerator
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
        refractive_index = 1
        if "refractive_index" in m:
            refractive_index = m["refractive_index"]
        
        mat = Material(m["name"], m["reflection"], m["refraction"], refractive_index)
        materials.append(mat)

    default_material = Material("default", 0, 0)
    material_names = list(map(lambda x: x.name, materials))

    sampling_types = obj["sampling_types"]
    sampling_index = settings["sampling_type"]
    if len(sampling_types) <= sampling_index:
        sampling_index = 0

    accelerator = None
    accelerator_types = obj["accelerator_types"]
    if "accelerator_type" in settings:
        accelerator_type = settings["accelerator_type"]
        accelerator_name = accelerator_types[accelerator_type]
        if accelerator_name == "BVHAccelerator":
            accelerator = BVHAccelerator([])
        else:
            accelerator = ListAccelerator([])
    else:
        accelerator = ListAccelerator([])

    lambert_shader = LambertShader(
        accelerator,
        lights,
        settings["ambient_ray_count"],
        settings["ambient_coefficient"],
        settings["ambient_occlusion"],
        sampling_types[sampling_index],
    )

    objects = []
    for s in obj["spheres"]:
        shader = None
        if s["shader_type"] == "Lambert":
            shader = lambert_shader
        t = "default"
        if "type" in s:
            t = s["type"]

        material = default_material
        if "material" in s and s["material"] in material_names:
            material = materials[material_names.index(s["material"])]

        objects.append(
            Sphere(
                s["posX"],
                s["posY"],
                s["posZ"],
                s["radius"],
                s["color"]["r"] / 255,
                s["color"]["g"] / 255,
                s["color"]["b"] / 255,
                material,
                shader,
                t,
            )
        )

    for o in obj["meshes"]:
        specs = generate_vertices_with_tn(o["filename"])
        shader = None
        if o["shader_type"] == "Lambert":
            shader = lambert_shader
        t = "default"
        if "type" in o:
            t = o["type"]

        material = default_material
        if "material" in o and o["material"] in material_names:
            material = materials[material_names.index(o["material"])]

        objects.append(
            Mesh(specs[0], specs[1], specs[2], specs[3], material, shader, t)
        )

    if "generators" in obj and len(obj["generators"]) > 0:
        for g in obj["generators"]:
            box = AABB()
            bmin = g["boundary"]["min"]
            box.min = Vector3f(bmin["x"], bmin["y"], bmin["z"])
            bmax = g["boundary"]["max"]
            box.max = Vector3f(bmax["x"], bmax["y"], bmax["z"])
            color = RGBA(g["color"]["r"], g["color"]["g"], g["color"]["b"]) if "color" in g else None

            material = default_material
            if "material" in g and g["material"] in material_names:
                material = materials[material_names.index(g["material"])]

            gen = SphereGenerator(g["radius"]["min"], g["radius"]["max"],box, lambert_shader, color, material, g["seed"])
            for _ in range(g["count"]):
                objects.append(gen.generate())

    accelerator.objects = objects
    accelerator.initialize()

    return Scene(
        settings["xres"],
        settings["yres"],
        camera,
        accelerator,
        lights,
        settings["worker_count"],
        settings["bounce_count"],
    )
