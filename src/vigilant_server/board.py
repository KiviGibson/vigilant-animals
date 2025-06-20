from .node import Node
from typing import Self, Any
from .card import Unit, Card


class Player(Node):
    MAX_HEALTH = 20

    def __init__(
        self,
        id: int,
        websocket,
        children: list[Node] | None = None,
        deck: list[Node] | None = None,
    ):
        super().__init__("Player", children if children is not None else [])
        self.hand = []
        self.draw_pile = [] if deck is None else deck
        self.health = self.MAX_HEALTH
        self.websocket = websocket
        self.honey_combs = 1
        self.honey = 1
        self.id = id

    def draw(self, num: int = 1) -> None:
        for _ in range(num):
            if len(self.draw_pile) <= 0:
                return
            self.hand.append(self.draw_pile.pop())

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
                            if self.hand[card_index].cost > self.honey:
                                return {"action": "repeat"}
                            tasks.append(task)
                        res["action"] = "play"
                        res["index"] = response["index"]
                case "pass":
                    return {"action": "pass"}

        return res  # {"action: ["play", "pass", "activate"], index: 0, targets: [(self.hand, index)]"}

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


class Board(Node):
    def __init__(
        self,
        name="Board",
        board_size=5,
        children: list[Node] | None = None,
    ):
        super().__init__(name, children if children is not None else [])
        self.player_units: list[list] = [
            [None for _ in range(board_size)] for _ in range(2)
        ]
        self.players: list[Player] = []
        self.current: int = 0
        self.passed = False
        self.winner = -1
        self.turn = 1
        self.atack = True

    def add_player(self, player: Player) -> None:
        if len(self.players) >= 2:
            return
        self.add_child(player)
        self.players.append(player)

    async def loop(self) -> None:
        for player in self.players:
            player.draw(5)
        while self.winner == -1:
            move = await self.players[self.current].get_user_input()
            match move["action"]:
                case "play":
                    self.passed = False
                    self.play_card(
                        self.players[self.current].hand[move["index"]], move["targets"]
                    )
                    self.next_player()
                case "pass":
                    self.skip_turn()
                case _:
                    continue
            self.sync_game()

    def next_player(self) -> None:
        self.current = (self.current + 1) % 2

    def skip_turn(self) -> None:
        if not self.passed:
            self.passed = True
            self.next_player()
            return
        if self.atack:
            self.atack_phase()
        else:
            self.next_round()

    def atack_phase(self) -> None:
        atacker = self.turn % 2
        defender = 1 if atacker == 0 else 0
        for i in range(5):
            if isinstance(atacking_unit := self.player_units[atacker][i], Unit):
                defending_unit = self.player_units[defender][i]
                killed_unit = atacking_unit.strike(defending_unit)
                if not killed_unit:
                    continue
                self.player_units[defender][i] = None
                del defending_unit
        self.atack = False

    def next_round(self) -> None:
        self.turn += 1
        self.atack = True
        self.current = self.turn % 2
        for player in self.players:
            player.draw(1)

    def sync_game(self) -> None:
        board_data = [
            [unit.get_data() for unit in units] for units in self.player_units
        ]
        self.players[0].sync_board(board_data, self.players[1])
        self.players[1].sync_board(board_data, self.players[0])

    def get_unit(self, player_id, unit_index) -> Unit | None:
        if 0 <= unit_index <= 5:
            return self.player_units[player_id][unit_index]
        return None

    def add_unit(self, player_id: int, index: int, unit: Unit) -> None:
        self.player_units[player_id][index] = unit
        self.add_child(unit)

    def play_card(self, card: Card, targets: list[tuple[list, int]]) -> None:
        card.play(targets)


def create_board() -> Board:
    return Board(name="Board", board_size=5, children=[])
