from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .card import Unit
    from .board import Board
    from .player import Player

### BEARS


def gain_honey_comb(**kwargs) -> None:
    if "myself" not in kwargs:
        return
    unit: Unit = kwargs["myself"]
    board: Board = unit.get_board()
    board.players[unit.owner_id].honey_combs += 1


def fisher(**kwargs) -> None:
    if "myself" not in kwargs:
        return
    unit: Unit = kwargs["myself"]
    board: Board = unit.get_board()
    for i in board.player_units:
        for u in i:
            unit.strike(u)


def build_gain_stats(damage: int, health: int) -> Callable:
    def gain_stats(**kwargs) -> None:
        if "myself" not in kwargs:
            return
        unit: Unit = kwargs["myself"]
        unit.damage += damage
        unit.health += health

    return gain_stats


def wojtek_effect(**kwargs) -> None:
    if "myself" not in kwargs:
        return
    unit: Unit = kwargs["myself"]
    board: Board = unit.get_board()
    player: Player = board.players[unit.owner_id]
    for u in board.player_units[unit.owner_id]:
        if u.type == "fish":
            player.honey += 1
    player.honey = min(player.honey, player.honey_combs)
