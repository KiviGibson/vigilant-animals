from node import Node
from typing import List, Tuple
from card import Card
from enums import PlayerAction


class Player(Node):
    honey: int
    honey_comb: int
    hand: List[Card]
    id: int

    def __init__(self, children: List[Node] | None = None) -> None:
        super().__init__(children)

    def get_input(self) -> PlayerAction:
        current_action = PlayerAction.NoAction
        while current_action == PlayerAction.NoAction:
            player_text = input("make action:")
            description = ""
            match player_text.split(" "):
                case ["pass"]:
                    current_action = PlayerAction.Pass
                    description = "Player passed"
                case ["play", num, *args]:
                    try:
                        num = int(num)
                        pos = int(args[0])
                    except Exception:
                        pass
                    else:
                        current_action, description = self.play_card(num)
            print(description)
        return current_action

    def play_card(self, index: int) -> Tuple[PlayerAction, str]:
        card: Card = self.hand[index]
        if card.cost > self.honey:
            return PlayerAction.NoAction, "Not Enought Honey"
        return card.play()
