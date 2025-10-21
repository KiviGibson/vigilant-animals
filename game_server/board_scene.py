from board import Board
from game_state import *
from player import Player


def board_scene(player1, player2) -> Board:
    b = Board(
        [
            # States
            rs := RoundStart([]),
            re := RoundEnd([]),
            pt := PlayerTurn([]),
            ap := AtackPhase([]),
            sd := SpellShowDown([]),
            Node([Player([]), Player([])]),
            Node(),
        ],
        start_state=rs,
    )
    # States Connection Web
    rs.playerState = pt
    pt.atackPhase = ap
    pt.endRound = re
    ap.playerPhase = pt
    re.startRound = rs
    return b
