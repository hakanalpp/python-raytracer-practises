from ..shape import Shape, AABB


class Node:
    def __init__(
        self,
        box: "AABB" = None,
        is_leaf: bool = True,
        parent: "Node" = None,
        object: "Shape" = None,
    ) -> None:
        self.box = box
        self.object = object
        self.parent = parent
        self.is_leaf = is_leaf
        self.children: list["Node"] = []

    def __repr__(self) -> str:
        return str(
            {
                "box": self.box,
                "object": self.object,
                "is_leaf": self.is_leaf,
                "children": self.children,
            }
        )
