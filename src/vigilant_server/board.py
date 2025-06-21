from .node import Node
from .card import Unit, Card
from .player import Player


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
            if isinstance((atacking_unit := self.player_units[atacker][i]), Unit):
                defending_unit = self.player_units[defender][i]
                damage = atacking_unit.strike(defending_unit)
                print(damage)
                if damage == -1:
                    self.player_units[defender][i] = None
                    del defending_unit
                elif damage > 0:
                    self.players[defender].health -= damage
        self.atack = False
        self.passed = False

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
        p = card.parent
        if isinstance(p, Player):
            p.discard(card)
        card.play(targets)


def create_board() -> Board:
    return Board(name="Board", board_size=5, children=[])
