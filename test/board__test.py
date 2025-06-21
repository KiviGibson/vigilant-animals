from unittest import TestCase, main
from vigilant_server import Player, Board, units


class BoardTest(TestCase):
    def test_add_units(self):
        board = Board()
        board.add_unit(0, 3, units.base_unit())
        board.add_unit(1, 4, units.base_unit())
        self.assertEqual(board.player_units[0][3].name, "Unit")
        self.assertEqual(board.player_units[1][4].name, "Unit")

    def test_play_a_card(self):
        board = Board()
        board.add_player(
            Player(0, None, children=(c := [units.base_unit_card()]), deck=c)
        )
        board.players[0].draw(1)
        board.play_card(board.players[0].hand[0], [(board.player_units[0], 0)])
        self.assertEqual(board.players[0].honey, 0)
        self.assertNotEqual(board.player_units[0][0], None)

    def test_atack(self):
        board = Board()
        board.add_player(
            Player(
                0,
                None,
                children=(d1 := [units.base_unit_card() for _ in range(10)]),
                deck=d1,
            )
        )
        board.add_player(
            Player(
                1,
                None,
                children=(d2 := [units.base_unit_card() for _ in range(10)]),
                deck=d2,
            )
        )
        for player in board.players:
            player.draw(3)
        board.next_player()
        board.play_card(
            board.players[board.current].hand[0],
            [(board.player_units[board.current], 0)],
        )
        board.atack_phase()
        self.assertNotEqual(
            board.players[0].get_stats()[2], board.players[1].get_stats()[2]
        )

    def test_turn_workflow(self):
        board = Board()
        board.add_player(Player(0, None))
        board.add_player(Player(1, None))
        self.assertEqual(board.turn, 1)
        self.assertEqual(board.atack, True)
        board.skip_turn()
        board.skip_turn()
        self.assertEqual(board.atack, False)
        board.skip_turn()
        board.skip_turn()
        self.assertEqual([board.atack, board.turn], [True, 2])


if __name__ == "__main__":
    main()
