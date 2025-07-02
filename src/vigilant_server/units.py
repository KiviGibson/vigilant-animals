from .card import Unit, Card, Summoner
from typing import Callable
from .unit_effect import *


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


def bearer_of_honey() -> Unit:
    return Unit(
        damage=1,
        health=4,
        name="Bearer of Honey",
        desc="On Summon gain honey comb",
        children=[],
        on_spawn=[gain_honey_comb],
    )


def bearer_of_honey_card() -> Card:
    return Card(
        name="Bearer of honey",
        desc="On Summon gain honey comb",
        honey_cost=4,
        children=[Summoner(unit=bearer_of_honey, children=[])],
    )


def salmon_slapper() -> Unit:
    return Unit(
        damage=6,
        health=6,
        name="Salmon Slapper",
        desc="I strike All fishes. I gain +1| +1 when I Strike",
        children=[],
        on_strike=[build_gain_stats(1, 1)],
        on_spawn=[fisher],
    )


def salmon_slapper_card() -> Card:
    return Card(
        name="Salmon Slapper",
        desc="I strike ALL fishes. I Gain +1| +1 when I strike",
        honey_cost=6,
        children=[Summoner(unit=salmon_slapper, children=[])],
    )


def wojtek() -> Unit:
    return Unit(
        damage=2,
        health=4,
        name="Wojtek",
        desc="On Summon refil honey equal to amount of friendly fish",
        children=[],
        on_spawn=[wojtek_effect],
    )


def wojtek_card() -> Card:
    return Card(
        name="Wojtek",
        desc="On Summon refil honey equal to amount of friendly fish",
        honey_cost=3,
        children=[Summoner(unit=wojtek, children=[])],
    )


listed_units: list[Callable] = [base_unit_card]
