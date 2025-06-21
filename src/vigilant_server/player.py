from .node import Node
from typing import Any, Self


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

    def discard(self, card: Node) -> None:
        self.hand.remove(card)

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
