from typing import List
from .node import Node

class BoardState(Node):
    def __init__(self, children: List[Node]|None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        pass

class Board(Node):
    def __init__(self, children: List[Node]|None = None) -> None:
        super().__init__(children)
        self.current_player: int = 0
        self.round_number: int = 0
    def round(self) -> None:
        pass

    def turn(self) -> None:
        pass

