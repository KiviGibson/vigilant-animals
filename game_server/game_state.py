from node import Node
from typing import List, type_check_only
if type_check_only:
    from board import Board
class BoardState(Node):
    def __init__(self, children: List[Node]|None = None) -> None:
        super().__init__(children)

    def control(self) -> None: 
        pass


class RoundStart(BoardState):
    def __init__(self, children: List[Node]|None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        pass

