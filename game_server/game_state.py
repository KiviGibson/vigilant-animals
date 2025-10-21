from node import Node
from typing import List, type_check_only, Self


class BoardState(Node):
    lastState: Node

    def __init__(self, children: List[Node] | None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        pass

    def start_state(self, before: Node | None) -> None:
        self.lastState = before if before is not None else Node()
        self.control()

    def end_state(self, next: Node) -> None:
        board = self.parent
        board.change_state(next)  # type: ignore


class RoundStart(BoardState):
    playerState: BoardState

    def __init__(self, children: List[Node] | None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        root = self.parent
        if isinstance(root, Node):
            root.round_start()
        self.end_state(self.playerState)


class PlayerTurn(BoardState):
    atackPhase: BoardState
    endRound: BoardState

    def __init__(self, children: List[Node] | None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        pass  # TODO: allow Player interaction
        if True:  # TODO: make good system of swaping turns
            self.end_state(self.atackPhase)
        else:
            self.end_state(self.endRound)


class RoundEnd(BoardState):
    startRound: BoardState

    def __init__(self, children: List[Node] | None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        root = self.parent
        if isinstance(root, Node):
            root.round_end()
        self.end_state(self.startRound)


class AtackPhase(BoardState):
    playerPhase: BoardState

    def __init__(self, children: List[Node] | None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        pass  # TODO: Make units clash
        self.end_state(self.playerPhase)


class SpellShowDown(BoardState):
    def __init__(self, children: List[Node] | None = None) -> None:
        super().__init__(children)

    def control(self) -> None:
        pass  # TODO: create spell showdown system
        self.end_state(self.lastState)
