from .node import Node
from typing import Self, Callable, Any
from .player import Player


class CardEffect(Node):
    def __init__(self, children: list[Node] = [], task: dict[str, Any] | None = None):
        self.task = task if task is not None else dict()
        super().__init__("CardEffect", children)

    def get_task(self) -> dict:
        return self.task

    def play(self, player: Player, targets: list[tuple[list, int]]):
        pass


class Card(Node):
    def __init__(
        self, desc: str, name: str, honey_cost: int, children: list = []
    ) -> None:
        self.desc = desc
        self.name = name
        self.honey_cost = honey_cost
        super().__init__("Card", children)

    def get_task(self) -> list[dict[str, Any]]:
        res = []
        for child in self.children:
            if child.name == "CardEffect":
                res.append(child.get_task())
        return res

    def play(self, targets: list[tuple[list, int]] = []) -> None:
        if isinstance(self.parent, Player):
            self.parent.honey -= self.honey_cost
        for child in self.children:
            if child.name == "CardEffect":
                child.play(self.parent, targets)


class Unit(Node):
    def __init__(
        self,
        damage: int,
        health: int,
        name: str,
        desc: str,
        children: list = [],
        # Sygnały niczym w GODOT lista jest wywoływana po koleji gdy dany event zaistnieje
        # Implementacja Funkcji subskrybującej posiada wymóg **kwargs, by dla każdej funkcji można było wykonywać zadane checki
        on_spawn: list[Callable] | None = None,
        on_strike: list[Callable] | None = None,
        on_face_strike: list[Callable] | None = None,
        on_death: list[Callable] | None = None,
        on_kill: list[Callable] | None = None,
        on_atack: list[Callable] | None = None,
    ) -> None:
        self.damage = damage
        self.health = health
        self.desc = desc
        self.name = name
        self.owner: Player | None = None
        self.on_strike = on_strike
        self.on_face_strike = on_face_strike
        self.on_kill = on_kill
        self.on_death = on_death
        self.on_atack = on_atack
        super().__init__("Unit", children)
        if on_spawn is not None:
            for obs in on_spawn:
                obs(myself=self)

    def strike(self, striken: Self | None) -> int:
        if striken is None:
            return self.face_strike()
        if self.on_strike is not None:
            for obs in self.on_strike:
                obs(myself=self)
        if striken.damage_delt(self.damage):
            self.on_kill_event(defeated=striken, myself=self)
            return -1
        return 0

    def face_strike(self) -> int:
        if self.on_face_strike is not None:
            for obs in self.on_face_strike:
                obs(myself=self)
        return self.damage

    def damage_delt(self, damage, **kwargs) -> bool:
        self.health -= damage
        if self.health <= 0:
            self.on_death_event(
                myself=self, killer=kwargs["unit"] if "unit" in kwargs else None
            )
            return True
        return False

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "health": self.health,
            "damage": self.damage,
            "desc": self.desc,
        }

    def on_kill_event(self, **kwargs) -> None:
        if self.on_kill is None:
            return
        for func in self.on_kill:
            func(**kwargs)

    def on_death_event(self, **kwargs) -> None:
        if self.on_death is None:
            return
        for func in self.on_death:
            func(**kwargs)

    def on_atack_event(self, **kwargs) -> None:
        if self.on_atack is None:
            return
        for func in self.on_atack:
            func(myself=self, **kwargs)


class Summoner(CardEffect):
    def __init__(self, unit: Callable, children: list[Node] = []) -> None:
        self.stored_unit = unit  # funkcja tworząca jednostkę
        super().__init__(
            children,
            task={
                "type": "choose",
                "from": "self",
                "message": "choose yours empty unit slot",
            },
        )

    def play(self, player: Player, targets: list[tuple[list, int]]) -> None:
        unit = self.stored_unit()
        unit.owner = player
        target = targets.pop()  # [ (list, int) ]
        target[0][target[1]] = unit
