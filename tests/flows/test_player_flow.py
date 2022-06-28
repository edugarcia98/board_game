from unittest import TestCase
from unittest.mock import patch

from flows import PlayerFlow
from schemas import CautiousPlayer, ImpulsivePlayer
from tests import mocked_board, mocked_property


class TestMoveSpaces(TestCase):
    def setUp(self):
        self.player = ImpulsivePlayer()
        self.spaces = 2
        self.board = mocked_board()
        self.board_info = {
            "board": self.board,
            "board_size": len(self.board),
            "board_max_idx": len(self.board) - 1,
        }

        self.player_flow = PlayerFlow(self.player, self.spaces, **self.board_info)
    
    @patch("flows.player_flow.logger")
    def test_move_spaces_common(self, mocked_logger):
        self.player_flow._move_spaces()

        self.assertEqual(self.player_flow.property, self.board[2])
        self.assertEqual(self.player.position, 2)
        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} caiu em {self.board[2].name}."
        )
    
    @patch("flows.player_flow.logger")
    def test_move_spaces_complete_board(self, mocked_logger):
        self.player.position = 3
        self.player_flow.spaces = 4

        self.player_flow._move_spaces()

        self.assertEqual(self.player_flow.property, self.board[2])
        self.assertEqual(self.player.position, 2)
        self.assertEqual(self.player.amount, 400)
        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} caiu em {self.board[2].name}."
        )


class TestPlayerAction(TestCase):
    def setUp(self):
        self.player = ImpulsivePlayer()
        self.spaces = 2
        self.board = mocked_board()
        self.board_info = {
            "board": self.board,
            "board_size": len(self.board),
            "board_max_idx": len(self.board) - 1,
        }

        self.player_flow = PlayerFlow(self.player, self.spaces, **self.board_info)
    
    @patch("flows.player_flow.Player.buy_property")
    @patch("flows.player_flow.logger")
    def test_player_action_property_no_owner(self, mocked_logger, mocked_buy_property):
        self.player_flow.property = self.board[1]

        self.player_flow._player_action()

        self.assertTrue(mocked_buy_property.called)
        mocked_logger.info.assert_called_with(f"{self.board[1].name} não possui dono.")

    @patch("flows.player_flow.logger")
    def test_player_action_player_owns_property(self, mocked_logger):
        prop = self.board[1]
        prop.owner = self.player

        self.player_flow.property = prop

        self.player_flow._player_action()

        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} já é o dono de {prop.name}."
        )

    @patch("flows.player_flow.Player.pay_rent")
    @patch("flows.player_flow.logger")
    def test_player_action_property_has_owner(self, mocked_logger, mocked_pay_rent):
        another_player = CautiousPlayer()

        prop = self.board[1]
        prop.owner = another_player

        self.player_flow.property = prop

        self.player_flow._player_action()

        self.assertTrue(mocked_pay_rent.called)
        mocked_logger.info.assert_called_with(
            f"{another_player.profile_name} é o dono de {prop.name}. "
            f"{self.player.profile_name} deve pagar aluguel."
        )


class TestCheckPlayerAmount(TestCase):
    def setUp(self):
        self.player = ImpulsivePlayer()
        self.spaces = 2
        self.board = mocked_board()
        self.board_info = {
            "board": self.board,
            "board_size": len(self.board),
            "board_max_idx": len(self.board) - 1,
        }

        self.player_flow = PlayerFlow(self.player, self.spaces, **self.board_info)
    
    @patch("flows.player_flow.Player.invalidate")
    def test_check_player_amount_positive(self, mocked_invalidate):
        self.player_flow._check_player_amount()

        self.assertFalse(mocked_invalidate.called)
    
    @patch("flows.player_flow.logger")
    @patch("flows.player_flow.Player.invalidate")
    def test_check_player_amount_negative(self, mocked_invalidate, mocked_logger):
        self.player.amount = -50

        self.player_flow._check_player_amount()
        
        self.assertTrue(mocked_invalidate.called)
        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} está com saldo negativo, então está "
            f"desclassificado."
        )


class TestExecute(TestCase):
    def setUp(self):
        self.player = ImpulsivePlayer()
        self.spaces = 2
        self.board = mocked_board()
        self.board_info = {
            "board": self.board,
            "board_size": len(self.board),
            "board_max_idx": len(self.board) - 1,
        }

        self.player_flow = PlayerFlow(self.player, self.spaces, **self.board_info)
    
    @patch("flows.player_flow.PlayerFlow._check_player_amount")
    @patch("flows.player_flow.PlayerFlow._player_action")
    @patch("flows.player_flow.PlayerFlow._move_spaces")
    def test_execute(self, mocked_move_spaces, mocked_action, mocked_check_amount):
        self.player_flow.execute()

        self.assertTrue(mocked_move_spaces.called)
        self.assertTrue(mocked_action.called)
        self.assertTrue(mocked_check_amount.called)
