from unittest import TestCase, main
from vigilant_server import Board, units
from typing import Any


class BoardTest(TestCase):
    def test_add_units(self):
        board = Board()
        board.add_unit(0, 3, units.base_unit())
        board.add_unit(1, 4, units.base_unit())
        board_units = board.get_units_data()
        self.assertEqual(board_units[0][3]["name"], "Unit")
        self.assertEqual(board_units[1][4]["name"], "Unit")

    def test_play_a_card(self):
        pass


if __name__ == "__main__":
    main()
