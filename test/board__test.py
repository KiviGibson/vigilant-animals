from unittest import TestCase, main
from vigilant_server import Board, units
from typing import Any


class BoardTest(TestCase):
    def test_add_units(self):
        board = Board()
        board.add_unit(0, 3, units.base_unit())
        board.add_unit(1, 4, units.base_unit())
        self.assertEqual(board.player_units[0][3].name, "Unit")
        self.assertEqual(board.player_units[1][4].name, "Unit")

    def test_play_a_card(self):
        board = Board()
        board.add_unit(0, 3, units.base_unit())
        board.play_card(units.base_unit_card(), [(board.player_units[1], 3)])
        self.assertEqual(
            [
                o.get_info()["name"] if o is not None else ""
                for o in board.player_units[0]
            ],
            [
                o.get_info()["name"] if o is not None else ""
                for o in board.player_units[1]
            ],
        )


if __name__ == "__main__":
    main()
