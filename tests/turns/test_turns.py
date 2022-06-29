from unittest import TestCase
from unittest.mock import call, patch

from game import full_game
from game.turns import _game_round, _get_winner_when_timeout, _initialize_players
from schemas import CautiousPlayer, DemandingPlayer, ImpulsivePlayer, Player
from tests import mocked_board


class TestInitializePlayer(TestCase):
    def test_initialize_players(self):
        players = _initialize_players()

        for player in players:
            self.assertIsInstance(player, Player)


class TestGameRound(TestCase):
    def setUp(self):
        self.player = ImpulsivePlayer()
        self.players = [self.player]
        self.board = mocked_board()

        self.board_info = {
            "board": self.board,
            "board_size": len(self.board),
            "board_max_idx": len(self.board) - 1,
        }
    
    @patch("game.turns.PlayerFlow")
    @patch("game.turns.choice")
    def test_game_round(self, mocked_choice, mocked_player_flow):
        mocked_choice.return_value = 2

        _game_round(self.players, **self.board_info)

        mocked_player_flow.assert_called_with(
            player=self.player,
            spaces=2,
            **self.board_info,
        )
        self.assertTrue(mocked_player_flow.return_value.execute.called)


class TestGetWinnerWhenTimeout(TestCase):
    def setUp(self):
        self.player1 = ImpulsivePlayer()
        self.player2 = CautiousPlayer()

        self.player1.amount = 500
        self.player2.amount = 400

        self.players = [self.player1, self.player2]
    
    def test_get_winner_when_timeout_unique(self):
        winner = _get_winner_when_timeout(self.players)

        self.assertEqual(winner, self.player1.profile_name)
    
    def test_get_winner_when_timeout_more_than_one(self):
        player3 = DemandingPlayer()
        player3.amount = 500

        self.players.append(player3)

        winner = _get_winner_when_timeout(self.players)

        self.assertEqual(winner, self.player1.profile_name)
    

class TestFullGame(TestCase):
    def setUp(self):
        self.game_number = 1

        self.player = ImpulsivePlayer()
        self.players = [self.player]
    
    @patch("game.turns.logger")
    @patch("game.turns._game_round")
    @patch("game.turns._initialize_players")
    def test_full_game_with_winner(
        self, mocked_initialize, mocked_game_round, mocked_logger,
    ):
        mocked_initialize.return_value = self.players
        mocked_game_round.return_value = True

        game_metrics = full_game(self.game_number)

        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} é o vencedor."
        )
        
        expected_metrics = {
            "winner": self.player.profile_name,
            "turns": 1,
            "timeout": False,
        }
        self.assertEqual(game_metrics, expected_metrics)
    
    @patch("game.turns.logger")
    @patch("game.turns._game_round")
    @patch("game.turns._initialize_players")
    def test_full_game_draw(
        self, mocked_initialize, mocked_game_round, mocked_logger,
    ):
        player2 = CautiousPlayer()
        self.player.amount = 400
        player2.amount = 300

        self.players.append(player2)

        mocked_initialize.return_value = self.players
        mocked_game_round.return_value = True

        game_metrics = full_game(self.game_number)

        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} é o vencedor."
        )
        
        self.assertTrue(
            call("Empate! Validando jogador com mais saldo.")
            in mocked_logger.info.mock_calls
        )

        expected_metrics = {
            "winner": self.player.profile_name,
            "turns": 1000,
            "timeout": True,
        }
        self.assertEqual(game_metrics, expected_metrics)
