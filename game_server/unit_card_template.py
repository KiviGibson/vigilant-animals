from unit_card import UnitCard
from unit import Unit

def unit(name: str, desc: str, damage: int, health: int, position: int, owner: int) -> Unit:
    return Unit(name, desc, damage, health, position, owner)

def unit_card() -> UnitCard:
    unit_c = UnitCard(%name%, %cost%, %health%, %damage%, %desc%, unit, children=[])
    return unit_c
