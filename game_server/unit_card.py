from card import Card
from node import Node
from typing import List, Callable
from unit import Unit
from enums import PlayerAction


class UnitCard(Card):
    unit_name: str
    unit_desc: str
    health: int
    damage: int
    summon_func: Callable

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

    def play(self, pos: int = 0) -> PlayerAction:
        unit: Unit = self.summon_func(
            self.name, self.health, self.damage, self.desc, self.unit_addons
        )
        return (
            PlayerAction.UnitCardPlayed,
            f"{self.name} has been summoned on position {pos}.",
        )
