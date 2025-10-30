from typing import List, Self, Type


class Node:
    def __init__(self, children: List[Node] | None = []):  # type: ignore
        self.parent: Node | None = None
        self.children: List[Node] = [] if children is None else children
        for child in self.children:
            child.parent = self

    def reparent(self, new_parent: Node) -> None:  # type: ignore
        if self.parent is not None:
            self.parent.children.remove(self)
        self.parent = new_parent
        self.parent.children.append(self)  # type: ignore

    def get_node(self, type: Type) -> Node | None:  # type: ignore
        if isinstance(self, type):
            return self
        elif self.parent is None:
            return None
        self.parent.get_node(type)

    def round_start(self) -> None:
        for child in self.children:
            child.round_start()

    def round_end(self) -> None:
        for child in self.children:
            child.round_end()
