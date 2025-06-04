from node import Node
from card import PlaceType
from typing import Self
from card import Unit


class Player(Node):
    def __init__(self, id: int, websocket, children: list[Node] = []):
        super().__init__("Player", children)
        self.hand = []
        self.draw_pile = []
        self.health = 20
        self.websocket = websocket
        self.id = id

    def get_stats(self) -> tuple[int, int, int]:
        return len(self.hand), len(self.draw_pile), self.health

    def get_user_input(self, message: str, type: PlaceType) -> int:
        # check if correct then give final answer in while loop
        return 0

    def sync_board(self, board_state: list[list[dict]], other: Self) -> None:
        enemy_data = other.get_stats()
        my_data = self.get_stats()
        game_state: dict = {
            "enemy": {
                "health": enemy_data[2],
                "cards in hand": enemy_data[0],
                "cards in deck": enemy_data[1],
            },
            "self": {
                "health": my_data[2],
                "cards in hand": my_data[0],
                "cards in deck": my_data[1],
            },
            "board": {
                "enemy_units": board_state[other.id],
                "my_units": board_state[self.id],
            },
        }
        # send data to client


class Turn(Node):
    def __init__(self, children: list[Node] = []):
        super().__init__("Turn", children)
        self.round_counter = 1
        self.active_player = 0


class Board(Node):
    def __init__(
        self, name="Board", player_units: list[Node] = [], children: list[Node] = []
    ):
        super().__init__(name, children)
        self.player_units = player_units
        self.players: list[Player] = []

    def add_player(self, player: Player) -> None:
        if len(self.players) >= 2:
            return
        self.add_child(player)
        self.players.append(player)

    def sync_game(self) -> None:
        board_data = self.get_units_data()
        self.players[0].sync_board(board_data, self.players[1])
        self.players[1].sync_board(board_data, self.players[0])

    def get_units_data(self) -> list[list[dict]]:
        res = []
        for units in self.player_units:
            unit_data = []
            for unit in units.children:
                if unit is None:
                    unit_data.append(None)
                    continue
                unit_data.append(unit.get_info())
            res.append(unit_data)
        return res

    def add_unit(self, player_id: int, index: int, unit: Unit) -> None:
        self.player_units[player_id].children[index] = unit


def create_board(name) -> Board:
    return Board(
        name=name,
        children=[
            p1u := Node(name="Player1_Units", children=[None for _ in range(5)]),
            p2u := Node(name="Player2_Units", children=[None for _ in range(5)]),
        ],
        player_units=[p1u, p2u],
    )
