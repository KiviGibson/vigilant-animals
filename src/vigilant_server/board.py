from .node import Node
from typing import Self, Any
from .card import Unit


class Player(Node):
    MAX_HEALTH = 20

    def __init__(self, id: int, websocket, children: list[Node] | None = None):
        super().__init__("Player", children if children is not None else [])
        self.hand = []
        self.draw_pile = []
        self.health = self.MAX_HEALTH
        self.websocket = websocket
        self.id = id

    def get_stats(self) -> tuple[int, int, int]:
        return len(self.hand), len(self.draw_pile), self.health

    async def get_user_input(self) -> dict[str, Any]:
        tasks = [
            {
                "type": "play",
                "from": "cards",
                "message": "pick a card or (P)ass",
                "optional": True,
            }
        ]
        res = {}
        while len(tasks) != 0:
            await self.websocket.send(tasks[0])
            response = await self.websocket.recv()
            if (
                response["type"] != tasks[0]["type"]
                or response["from"] != tasks[0]["from"]
            ):
                continue
            match response["type"]:
                case "play":
                    card_index = response["index"]
                    if card_index < len(self.hand):
                        for task in self.hand[card_index].get_tasks():
                            tasks.append(task)
                        res["action"] = "play"
                        res["index"] = response["index"]
                case "pass":
                    return {"action": "pass"}
                case "target":
                    if response["from"] in ["self", "enemy"]:
                        board = self.get_board()
                        if not isinstance(board, Board):
                            continue
                        if (
                            o := board.get_unit((self.id + 1) % 2, response["index"])
                        ) is None:
                            continue
                        res["targets"].append(o)
                    elif response["from"] == "pass" and "optional" in tasks[0]:
                        res["targets"].append(None)
                    else:
                        if response["index"] > len(self.hand):
                            continue
                        res["targets"].append(self.hand[response["index"]])
        return res

    def sync_board(self, board_state: list[list[dict]], other: Self) -> None:
        enemy_data = other.get_stats()
        my_data = self.get_stats()
        game_state: dict = {
            "type": "sync",
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
        self.websocket.send(game_state)


class Turn(Node):

    ROUND_START = 0
    PRE_ATACK = 1
    POST_ATACK = 2
    ROUND_END = 3

    def __init__(self, children: list[Node] | None = None):
        super().__init__("Turn", children if children is not None else [])
        self.round_counter: int = 1
        self.active_player: int = 0
        self.passed: bool = False
        self.round_state: int = self.ROUND_START

    def action(self, passed: bool) -> tuple[int, int]:
        if not passed:
            self.passed = False
        elif self.passed:
            self.round_state += 1
        else:
            self.passed = True
        self.active_player = (self.active_player + 1) % 2
        return self.round_state, self.active_player

    def next_state(self) -> None:
        self.state = (self.state + 1) % 4


class Board(Node):
    def __init__(
        self,
        name="Board",
        board_size=5,
        children: list[Node] | None = None,
        turn_clock: Turn | None = None,
    ):
        super().__init__(name, children if children is not None else [])
        self.player_units: list[list] = [
            [None for _ in range(board_size)] for _ in range(2)
        ]
        self.players: list[Player] = []
        self.turn = turn_clock if turn_clock is not None else Turn()
        self.winner = -1

    def add_player(self, player: Player) -> None:
        if len(self.players) >= 2:
            return
        self.add_child(player)
        self.players.append(player)

    async def loop(self) -> None:
        while self.winner == -1:
            move = await self.players[self.turn.active_player].get_user_input()
            match move["type"]:
                case "play":
                    self.turn.action(False)
                    self.players[self.turn.active_player].hand[move["index"]].play(
                        move["targets"]
                    )
                case "pass":
                    self.turn.action(True)

    def sync_game(self) -> None:
        board_data = self.get_units_data()
        self.players[0].sync_board(board_data, self.players[1])
        self.players[1].sync_board(board_data, self.players[0])

    def get_unit(self, player_id, unit_index) -> Unit | None:
        if 0 <= unit_index <= 5:
            return self.player_units[player_id][unit_index]
        return None

    def get_units_data(self) -> list[list[dict]]:
        res = [
            [
                unit.get_info() if unit is not None else {"info": "Empty"}
                for unit in units
            ]
            for units in self.player_units
        ]
        return res

    def add_unit(self, player_id: int, index: int, unit: Unit) -> None:
        self.player_units[player_id][index] = unit
        self.add_child(unit)


def create_board() -> Board:
    return Board(name="Board", children=[tc := Turn()], turn_clock=tc)
