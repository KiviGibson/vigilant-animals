from node import Node
from typing import Self, Callable
from enum import Enum


class Card(Node):
    def __init__(
        self,
        desc: str,
        name: str,
        play: CardEffect,
        children: list = [],
    ) -> None:
        self.desc = desc
        self.name = name
        self.play = play
        super().__init__(children)


class Unit(Node):
    def __init__(
        self,
        damage: int,
        health: int,
        name: str,
        desc: str,
        children: list = [],
        on_spawn: Callable | None = None,
        on_strike: Callable | None = None,
        on_face_strike: Callable | None = None,
    ) -> None:
        self.damage = damage
        self.health = health
        self.desc = desc
        self.on_strike = on_strike
        self.name = name
        self.on_face_strike = on_face_strike
        super().__init__(children)
        if on_spawn is not None:
            on_spawn()

    def strike(self, striken: Self | None) -> None:
        if striken is None:
            return
        striken.health -= self.damage
        if self.on_strike is not None:
            self.on_strike()

    def face_strike(self) -> None:
        if self.on_face_strike is not None:
            self.on_face_strike()


class CardEffect(Node):
    def __init__(self, children: list[Node] = []):
        super().__init__(children)

    def play(self) -> None:
        pass


class Summoner(CardEffect):
    def __init__(self, unit: Callable, children: list[Node] = []) -> None:
        self.stored_unit = unit
        super().__init__(children)

    def play(self) -> None:
        unit_list, index = get_place(PlaceType.EMPTY_ALLY_PLACE)
        # Choose place to summon unit
        unit: Unit = self.stored_unit()
        unit_list[index] = unit


class PlaceType(Enum):
    EMPTY_ALLY_PLACE = 0
    ALLY_UNIT = 1
    ENEMY_UNIT = 2
    ALLY_HAND_INDEX = 3


def get_place(ptype: PlaceType) -> tuple[list, int]:
    match ptype:
        case PlaceType.EMPTY_ALLY_PLACE:
            return
