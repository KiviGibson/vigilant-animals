from node import Node


class Keyword(Node):
    def __init__(self, children: list[Node] = []):
        super().__init__(children)


class Fly(Keyword):
    def __init__(self, children: list[Node] = []):
        super().__init__(children)
