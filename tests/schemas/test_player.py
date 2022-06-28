from unittest import TestCase
from unittest.mock import patch

from schemas import (
    CautiousPlayer,
    DemandingPlayer,
    ImpulsivePlayer,
    RandomPlayer,
)
from tests import mocked_board, mocked_property


class TestPlayer(TestCase):
    def setUp(self):
        self.player = ImpulsivePlayer()
        self.initial_amount = self.player.amount

        self.property = mocked_property()
        self.board = mocked_board()
    
    @patch("schemas.player.logger")
    @patch("schemas.player.ImpulsivePlayer._will_buy_property")
    def test_buy_property_cannot(self, mocked_will_buy_property, mocked_logger):
        mocked_will_buy_property.return_value = False

        self.player.buy_property(self.property)

        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} não pode comprar {self.property.name}."
        )
    
    @patch("schemas.player.logger")
    @patch("schemas.player.ImpulsivePlayer._will_buy_property")
    def test_buy_property_success(self, mocked_will_buy_property, mocked_logger):
        mocked_will_buy_property.return_value = True

        self.player.buy_property(self.property)

        self.assertEqual(self.property.owner, self.player)
        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} comprou {self.property.name}."
        )
    
    def test_pay_rent(self):
        another_player = RandomPlayer()
        self.property.owner = another_player

        self.player.pay_rent(self.property)

        self.assertEqual(
            self.player.amount, (self.initial_amount - self.property.rent_cost)
        )
        self.assertEqual(
            another_player.amount, (self.initial_amount + self.property.rent_cost)
        )
    
    @patch("schemas.player.logger")
    def test_invalidate_without_properties(self, mocked_logger):
        self.player.invalidate(self.board)

        self.assertFalse(self.player.active)
        self.assertFalse(mocked_logger.called)
    
    @patch("schemas.player.logger")
    def test_invalidate_with_properties(self, mocked_logger):
        board_item = self.board[0]

        board_item.owner = self.player
        self.player.invalidate(self.board)

        self.assertFalse(self.player.active)
        self.assertIsNone(board_item.owner)

        mocked_logger.info.assert_called_with(
            f"{self.player.profile_name} não é mais dono de {board_item.name}."
        )


class TestImpulsivePlayer(TestCase):
    def setUp(self):
        self.player = ImpulsivePlayer()
        self.property = mocked_property()
    
    def test_will_buy_property_true(self):
        result = self.player._will_buy_property(self.property)

        self.assertTrue(result)

    def test_will_buy_property_false(self):
        self.player.amount = 10
        result = self.player._will_buy_property(self.property)

        self.assertFalse(result)


class TestDemandingPlayer(TestCase):
    def setUp(self):
        self.player = DemandingPlayer()
        self.property = mocked_property()
    
    def test_will_buy_property_true(self):
        self.property.rent_cost = 100
        result = self.player._will_buy_property(self.property)

        self.assertTrue(result)

    def test_will_buy_property_false(self):
        self.property.rent_cost = 10
        result = self.player._will_buy_property(self.property)

        self.assertFalse(result)


class TestCautiousPlayer(TestCase):
    def setUp(self):
        self.player = CautiousPlayer()
        self.property = mocked_property()
    
    def test_will_buy_property_true(self):
        self.property.cost = 100
        result = self.player._will_buy_property(self.property)

        self.assertTrue(result)

    def test_will_buy_property_false(self):
        self.property.cost = 250
        result = self.player._will_buy_property(self.property)

        self.assertFalse(result)


class TestRandomPlayer(TestCase):
    def setUp(self):
        self.player = RandomPlayer()
        self.property = mocked_property()
    
    @patch("schemas.player.random.getrandbits")
    def test_will_buy_property_true(self, mocked_random_value):
        mocked_random_value.return_value = 1
        
        result = self.player._will_buy_property(self.property)

        self.assertTrue(result)

    @patch("schemas.player.random.getrandbits")
    def test_will_buy_property_false(self, mocked_random_value):
        mocked_random_value.return_value = 0

        result = self.player._will_buy_property(self.property)

        self.assertFalse(result)
