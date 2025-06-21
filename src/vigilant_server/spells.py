from card import Card
from typing import Callable
import spell_effect


def flight() -> Card:
    return Card(
        cost=2,
        name="flight",
        damage=0,
        health=0,
        desc="""Make unit fly (Flying units always hit face)""",
        play=None,
    )
