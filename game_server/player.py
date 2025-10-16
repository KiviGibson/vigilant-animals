from node import Node
from typing import List

class Player(Node):
    honey: int
    honey_comb: int
    hand: List[Card]
    id: int
    def __init__(self, children: List[Node]|None=None) -> None:
        super().__init__(children)
