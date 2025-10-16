from typing import List
from .node import Node
from .game_state  import BoardState
from player import Player
class Board(Node):
    def __init__(self, children: List[Node]|None = None, start_state: BoardState = None) -> None:
        super().__init__(children)
        self.current_player: int = 0
        self.round_number: int = 0
        self.state: BoardState = start_state
        self.players:List[Player] = []
    def round(self) -> None:
        pass

    def turn(self) -> None:
        pass

    def exit() -> None:
        pass
