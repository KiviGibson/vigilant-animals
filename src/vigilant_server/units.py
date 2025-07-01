from .card import Unit, Card, Summoner
from typing import Callable


def base_unit() -> Unit:
    return Unit(
        damage=2,
        health=2,
        name="Base Unit",
        desc="Base Unit Desc",
        children=[],
    )


def base_unit_card() -> Card:
    return Card(
        name="Base Card",
        desc="Base Desciption",
        honey_cost=1,
        children=[Summoner(unit=base_unit, children=[])],
    )


listed_units: list[Callable] = [base_unit_card]
