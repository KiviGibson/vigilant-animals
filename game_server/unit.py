from node import Node
from typing import List, Callable, Self


class Unit(Node):
    owner_id: int
    damage: int
    health: int
    pos_id: int
    name: str
    desc: str
    # SIGNALS
    on_spawn: List[Callable]
    on_attack: List[Callable]
    on_defend: List[Callable]
    on_strike: List[Callable]
    on_damaged: List[Callable]
    on_death_rattle: List[Callable]
    on_defeated_enemy: List[Callable]
    # MODIFIERS
    attack_mod: Callable | None
    take_damage_mod: Callable | None

    def __init__(
        self,
        name: str,
        desc: str,
        damage: int,
        health: int,
        position: int,
        owner: int,
        children: List[Node] | None = None,
        on_spawn: List[Callable] | None = None,
    ) -> None:
        self.owner_id = owner
        self.name = name
        self.desc = desc
        self.health = health
        self.damage = damage
        self.position = position
        self.on_spawn = on_spawn if on_spawn else []
        super().__init__(children)
        for fun in self.on_spawn:
            fun(self)

    def attack(self) -> None:
        for fun in self.on_attack:
            fun(self)

    def defend(self) -> None:
        for fun in self.on_defend:
            fun(self)

    def strike(self, other: Self) -> None:
        (
            other.take_damage(self, self.damage)
            if self.attack_mod is None
            else self.attack_mod(self, other, self.damage)
        )
        for fun in self.on_strike:
            fun(self, other)

    def take_damage(self, damage_dealer: Self, damage: int) -> None:
        self.health -= (
            damage
            if self.take_damage_mod is None
            else self.take_damage_mod(self, damage)
        )
        if self.health <= 0:
            self.death_rattle(damage_dealer)
        for fun in self.on_damaged:
            fun(self, damage_dealer, damage)

    def defeated_enemy(self, other: Self) -> None:
        for fun in self.on_defeated_enemy:
            fun(self, other)

    def death_rattle(self, killer: Self) -> None:
        for fun in self.on_death_rattle:
            fun(self, killer)

    def death(self) -> None:
        pass
