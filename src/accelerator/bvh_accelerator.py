# CENG 488 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# April 2022


from functools import cmp_to_key
from ..shape.bounding_box import AABB
from ..math import RGBA, Ray
from .node import Node
from .accelerator import Accelerator


class BVHAccelerator(Accelerator):
    def __init__(self, objects):
        super().__init__(objects)
        self.root = None

    def initialize(self):
        self.root = self.create_root()
        self.build_tree()

    def intersect_ray(self, ray: "Ray", distance=float("inf")):
        selected = (
            None,  # shape
            distance,  # distance
            RGBA(0, 0, 0),  # color
            None,  # ray
            None,  # normal
            None,  # hitPoint
        )  # (object, distance, color, ray, normal, hitPoint)

        node_stack = [self.root]
        while len(node_stack) > 0:
            node = node_stack.pop()

            if node.is_leaf:
                distance, color, normal, hitPoint = node.object.intersect(ray)
                if distance > 10e-3 and selected[1] - distance > 10e-3:
                    selected = (node.object, distance, color, ray, normal, hitPoint)
            else:
                if node.box.intersect(ray) != -1:
                    node_stack.extend(node.children)

        return selected

    def build_tree(self):
        nodes = [self.root]
        while len(nodes) > 0:
            node = nodes.pop(0)
            if len(node.children) > 2:
                node1, node2 = self.split_nodes(node)
                if not node1 is None:
                    nodes.append(node1)
                    nodes.append(node2)

    def create_root(self):
        root = Node(box=AABB())
        root.box.min = self.objects[0].bounding_box.min.clone()
        root.box.max = self.objects[0].bounding_box.max.clone()

        for obj in self.objects[1:]:
            root.box = root.box.union(obj.bounding_box)

        root.is_leaf = False

        for o in self.objects:
            node = Node(
                box=o.bounding_box,
                object=o,
                parent=root,
                is_leaf=True,
            )
            root.children.append(node)

        return root

    def split_nodes(self, node: "Node"):
        axis = self.get_sorting_axis(node.box)
        self.sort_node_children(node, axis)

        axis_center = (getattr(node.box.max, axis) + getattr(node.box.min, axis)) / 2
        axis_min = getattr(node.children[0].box.centeroid, axis)
        axis_max = getattr(node.children[-1].box.centeroid, axis)

        if axis_min == axis_center or axis_center == axis_max:
            return (None, None)

        left_node = Node(parent=node, is_leaf=False)
        right_node = Node(parent=node, is_leaf=False)

        for child_node in node.children:
            axis_value = getattr(child_node.box.centeroid, axis)

            if axis_value < axis_center:
                current_node = left_node
                child_node.parent = left_node
            else:
                current_node = right_node
                child_node.parent = right_node

            current_node.children.append(child_node)
            if current_node.box is None:
                current_node.box = child_node.box
            else:
                current_node.box = current_node.box.union(child_node.box)

        node.children = [left_node, right_node]

        return (left_node, right_node)

    def get_sorting_axis(self, box: "AABB"):
        lx = box.max.x - box.min.x
        ly = box.max.y - box.min.y
        lz = box.max.z - box.min.z
        axis = None
        if lx >= ly and lx >= lz:
            axis = "x"
        elif ly >= lx and ly >= lz:
            axis = "y"
        elif lz >= lx and lz >= ly:
            axis = "z"

        return axis

    def sort_node_children(self, node: "Node", axis):
        def comparator(n1, n2):
            v1 = getattr(n1.box.centeroid, axis)
            v2 = getattr(n2.box.centeroid, axis)
            return v1 - v2

        node.children.sort(key=cmp_to_key(comparator))
