from node import Node
from card import Unit, Card, Summoner


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
        children=[Summoner(unit=base_unit, children=[])],
    )
