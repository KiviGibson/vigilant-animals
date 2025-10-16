from node import Node
from typing import List
# Always child of Player before play
class Card(Node):
    cost: int
    def __init__(self, children: List[Node]|None = None, cost: int = 1) -> None:
        self.cost = cost
        super().__init__(children)

    def play(self) -> None:
        pass
