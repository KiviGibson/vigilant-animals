class Node:
    def __init__(self, name="Node", children: list = []) -> None:
        self.children = children
        self.name = name
        self.parent: Node | None = None
        for child in children:
            child.parent = self

    def add_child(self, child) -> None:
        child.parent = self
        self.children.append(child)

    def get_board(self):
        if self.name == "Board":
            return self
