from card import Card
from node import Node
from typing import List, Callable, Tuple
from unit import Unit
from enums import PlayerAction
from board import Board


class UnitCard(Card):
    unit_name: str
    unit_desc: str
    health: int
    damage: int
    summon_func: Callable
    on_play: List[Callable]

    def __init__(
        self,
        name: str,
        cost: int,
        health: int,
        damage: int,
        desc: str,
        summon_func: Callable,
        children: List[Node] | None = None,
    ) -> None:
        self.name = name
        self.cost = cost
        self.health = health
        self.damage = damage
        self.summon_func = summon_func
        self.desc = desc
        self.unit_addons: List[Node] = []
        super().__init__(children, cost)

    def play(self, pos: int = 0) -> Tuple[PlayerAction, str]:
        pos = int(input("choose unoccupied space:"))
        owner = self.parent.id  # type: ignore
        board: Board = self.get_node(Board)  # type: ignore
        if board.units[owner][pos] is not None:
            return PlayerAction.NoAction, "Spot occupied"
        for fun in self.on_play:
            fun()
        unit: Unit = self.summon_func(
            name=self.name,
            desc=self.desc,
            damage=self.damage,
            health=self.health,
            position=(pos, board.units[owner]),
            unit_addons=self.unit_addons,
            owner_id=owner,
        )
        return (
            PlayerAction.UnitCardPlayed,
            f"{self.name} has been summoned on position {pos}.",
        )
