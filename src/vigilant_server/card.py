from .node import Node
from typing import Self, Callable, Any


class CardEffect(Node):
    def __init__(self, children: list[Node] = [], task: dict[str, Any] | None = None):
        self.task = task if task is not None else dict()
        super().__init__("CardEffect", children)

    def get_task(self) -> dict:
        return self.task

    def play(self, targets: list[tuple[list, int]]):
        pass


class Card(Node):
    def __init__(
        self,
        desc: str,
        name: str,
        children: list = [],
    ) -> None:
        self.desc = desc
        self.name = name
        super().__init__("Card", children)

    def get_task(self) -> list[dict[str, Any]]:
        res = []
        for child in self.children:
            if child.name == "CardEffect":
                res.append(child.get_task())
        return res

    def play(self, targets: list[tuple[list, int]] = []) -> None:
        for child in self.children:
            if child.name == "CardEffect":
                child.play(targets)


class Unit(Node):
    def __init__(
        self,
        damage: int,
        health: int,
        name: str,
        desc: str,
        children: list = [],
        # Sygnały niczym w GODOT lista jest wywoływana po koleji gdy dany event zaistnieje
        on_spawn: list[Callable] | None = None,
        on_strike: list[Callable] | None = None,
        on_face_strike: list[Callable] | None = None,
    ) -> None:
        self.damage = damage
        self.health = health
        self.desc = desc
        self.on_strike = on_strike
        self.name = name
        self.on_face_strike = on_face_strike
        super().__init__("Unit", children)
        if on_spawn is not None:
            for obs in on_spawn:
                obs()

    def strike(self, striken: Self | None) -> None:
        if striken is None:
            self.face_strike()
            return
        striken.health -= self.damage
        if self.on_strike is not None:
            for obs in self.on_strike:
                obs()

    def face_strike(self) -> None:
        if self.on_face_strike is not None:
            for obs in self.on_face_strike:
                obs()

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "health": self.health,
            "damage": self.damage,
            "desc": self.desc,
        }


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

    def play(self, targets: list[tuple[list, int]]) -> None:
        unit = self.stored_unit()
        target = targets.pop()  # [ {place: list, index: int} ]
        target[0][target[1]] = unit
