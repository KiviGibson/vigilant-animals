import asyncio
import os
import sys
from websockets.asyncio.client import connect
from client.card import generate_board, Card
from typing import Callable
import pygame


class PlayerInfo:
    max_cards_on_board = 5

    def __init__(self):
        self.units_on_board: list[Card] = [
            Card.blank() for _ in range(self.max_cards_on_board)
        ]
        self.cards_in_deck: int = 40
        self.cards_in_hand: list[Card] = []
        self.action_token: bool = False
        self.mana: int = 1
        self.max_mana: int = 1
        self.health: int = 20


class Cursor:
    ally_lane = 9
    enemy_lane = 7
    card_lane = 0

    def __init__(self, data: list, identifier: str):
        self.data = data
        self.identifier = identifier
        self.index = 0

    def change_dataset(self, data: list, identifier: str, index: int = -1):
        self.data = data
        self.identifier = identifier
        self.index = self.index if index == -1 else index

    def start_index(self) -> int:
        container, side = self.identifier.split(" ")
        if container == "units":
            return self.ally_lane if side == "ally" else self.enemy_lane
        return self.card_lane


enemy: PlayerInfo
me: PlayerInfo
cursor: Cursor


def setup_game() -> None:
    global enemy, me, cursor
    enemy = PlayerInfo()
    me = PlayerInfo()
    cursor = Cursor(me.units_on_board, "units ally")
    pygame.init()


def render(message: str = "") -> None:
    os.system("clear" if sys.platform != "win32" else "cls")
    game_view: list[str] = generate_board(
        me.units_on_board, enemy.units_on_board, me.health, enemy.health
    )
    cursor_start: int = cursor.start_index()
    game_view[cursor_start] = (
        " " * (1 + cursor.index * 13)
        + ("/\\ /\\ /\\ /\\" if cursor_start == 7 else "\/ \/ \/ \/")
        + game_view[cursor_start][cursor.index * 13 + 12 :]
    )
    for line in game_view:
        print(line)
    print(message)


def get_key() -> str:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return pygame.key.name(event.key)


def wait() -> None:
    return


def base_cursor_movement() -> Callable:
    match get_key():
        case "j":
            if cursor.identifier.split(" ")[0] == "units":
                cursor.change_dataset(enemy.units_on_board, "units enemy")
            else:
                cursor.index = max(cursor.index - 1, 0)
        case "k":
            if cursor.identifier.split(" ")[0] == "units":
                cursor.change_dataset(me.units_on_board, "units ally")
            else:
                cursor.index = min(cursor.index + 1, len(cursor.data) - 1)
        case "h":
            if cursor.identifier.split(" ")[0] == "units":
                cursor.index = max(0, cursor.index - 1)
            else:
                cursor.change_dataset(me.units_on_board, "units ally", 4)
        case "l":
            if cursor.identifier.split(" ")[0] == "units":
                if cursor.index + 1 == len(cursor.data):
                    cursor.change_dataset(me.cards_in_hand, "cards ally", 0)
                else:
                    cursor.index += 1
    return base_cursor_movement


def game_loop() -> None:
    running = True
    message = ""
    state: Callable = base_cursor_movement
    d = pygame.display.set_mode((1, 1))
    while running:
        render(message)
        state = state()


if __name__ == "__main__":
    setup_game()
    game_loop()
