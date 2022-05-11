# CENG 488 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# April 2022


from functools import cmp_to_key
from typing import Union
from ..shape import AABB, Shape
from ..math import RGBA, Ray
from .accelerator import Accelerator


class Node:
    def __init__(
        self,
        box: "AABB" = None,
        coord: Union[str, float] = None,  # stored as [axis, point]
        left_child: "Node" = None,
        right_child: "Node" = None,
        parent: "Node" = None,
        shapes: list[Shape] = None,
    ) -> None:
        self.box = box
        self.coord = coord
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent
        self.shapes: list["Shape"] = shapes


class KDTreeAccelerator(Accelerator):
    def __init__(self, objects):
        super().__init__(objects)
        self.root = None
        self.empty_selected = [
            None,  # shape
            -1,  # distance
            RGBA(0, 0, 0),  # color
            None,  # ray
            None,  # normal
            None,  # hitPoint
        ]
        self.total_selected = [
            None,  # shape
            -1,  # distance
            RGBA(0, 0, 0),  # color
            None,  # ray
            None,  # normal
            None,  # hitPoint
        ]

    def initialize(self):
        self.root = self.create_root()
        self.build_tree(self.root)

    def intersect_ray(self, ray: "Ray", distance=float("inf")):
        selected = (
            None,  # shape
            distance,  # distance
            RGBA(0, 0, 0),  # color
            None,  # ray
            None,  # normal
            None,  # hitPoint
        )  # (object, distance, color, ray, normal, hitPoint)

        node_stack: list[Node] = [self.root]
        while len(node_stack) > 0:
            node = node_stack.pop()

            if node.left_child == None:
                temp = self.intersect_shapes(node.shapes, ray, distance)
                if temp[1] <= selected[1]:
                    selected = temp
            else:
                if node.box.intersect(ray) != -1:
                    node_stack.append(node.left_child)
                    node_stack.append(node.right_child)

        return selected

    def intersect_shapes(self, shapes: list[Shape], ray, distance):
        selected = (
            None,  # shape
            distance,  # distance
            RGBA(0, 0, 0),  # color
            None,  # ray
            None,  # normal
            None,  # hitPoint
        )
        for shape in shapes:
            distance, color, normal, hitPoint = shape.intersect(ray)
            if distance > 10e-3 and selected[1] - distance > 10e-3:
                selected = (shape, distance, color, ray, normal, hitPoint)

        return selected

    def build_tree(self, node: Node):  # True
        if not node.shapes or len(node.shapes) <= 1:
            return self.empty_selected

        left_child, right_child = self.create_child_nodes(node, node.coord[0])
        node.left_child = left_child
        node.right_child = right_child

        for shape in node.shapes:
            if self.is_shape_left(shape, node.coord):
                left_child.shapes.append(shape)
            else:
                right_child.shapes.append(shape)
        node.shapes = []
        self.build_tree(left_child)
        self.build_tree(right_child)

    def is_shape_left(self, shape: Shape, coord: Union[str, int]):  # True
        return getattr(shape.bounding_box.centeroid, coord[0]) <= coord[1]

    def create_child_nodes(self, node, axis):  # Kinda True
        left_box = AABB()
        left_box.min = node.box.min.clone()
        left_box.max = node.box.max.clone()
        setattr(left_box.max, axis, node.coord[1])

        right_box = AABB()
        right_box.min = node.box.min.clone()
        right_box.max = node.box.max.clone()
        setattr(right_box.min, axis, node.coord[1])

        new_axis = self.get_next_axis(axis)

        left_node = Node(
            box=left_box,
            coord=(new_axis, self.get_middle_point(left_box, new_axis)),
            parent=node,
            shapes=[],
        )
        right_node = Node(
            box=right_box,
            coord=(new_axis, self.get_middle_point(right_box, new_axis)),
            parent=node,
            shapes=[],
        )

        return left_node, right_node

    def get_next_axis(self, axis):
        return "x" if axis == "z" else "y" if axis == "x" else "z"

    def get_middle_point(self, box, axis):
        return (getattr(box.min, axis) + getattr(box.max, axis)) / 2

    def create_root(self):
        root = Node(box=AABB())
        root.box.min = self.objects[0].bounding_box.min.clone()
        root.box.max = self.objects[0].bounding_box.max.clone()

        for obj in self.objects[1:]:
            root.box = root.box.union(obj.bounding_box)

        root.coord = ("x", self.get_middle_point(root.box, "x"))
        root.shapes = self.objects

        return root
