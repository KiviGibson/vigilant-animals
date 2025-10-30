from typing import List, Tuple
from .node import Node
from .game_state import BoardState
from player import Player
from enums import PlayerAction
from unit import Unit


class Board(Node):
    def __init__(
        self, children: List[Node] | None = None, start_state: BoardState | None = None
    ) -> None:
        super().__init__(children)
        self.current_player: int = 0
        self.round_number: int = 0
        self.players: List[Player] = []
        self.passed: bool = False
        self.atacked: bool = False
        self.units: Tuple[List[Unit], List[Unit]] = ([], [])
        self.current_state: BoardState | None = None
        if start_state is not None:
            self.change_state(start_state)

    def player_input(self) -> PlayerAction:
        return self.players[self.current_player].get_input()

    def atack(self) -> None:
        for unit in self.units[self.round_number % 2]:
            unit.attack()
            defender = self.units[(self.round_number + 1) % 2][unit.position]
            if defender is not None:
                unit.strike(defender)

    def defend(self) -> None:
        for unit in self.units[(self.round_number + 1) % 2]:
            unit.defend()

    def new_round(self) -> None:
        self.round_number += 1
        self.passed = False
        self.atacked = False

    def change_state(self, next_state: BoardState) -> None:
        c = self.current_state
        self.current_state = next_state
        next_state.start_state(c)
