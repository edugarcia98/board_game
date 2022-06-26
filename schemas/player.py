import random

from abc import abstractmethod
from logger import logger


class Player:

    @abstractmethod
    def __init__(self):
        self.amount = 300
        self.position = 0
        self.profile_name = self.__class__.__name__
        self.active = True

    @abstractmethod
    def _will_buy_property(self, prop):
        return not prop.owner and self.amount >= prop.cost
    
    def buy_property(self, prop):
        if self._will_buy_property(prop):
            self.amount -= prop.cost
            prop.owner = self
            
            logger.info(f"{self.profile_name} comprou {prop.name}.")
        else:
            logger.info(f"{self.profile_name} não pode comprar {prop.name}.")
    
    def pay_rent(self, prop):
        self.amount -= prop.rent_cost
        prop.owner.amount += prop.rent_cost
        
        logger.info(
            f"{self.profile_name} pagou o aluguel de {prop.name} a "
            f"{prop.owner.profile_name}."
        )
    
    def invalidate(self, board):
        for prop in board:
            if prop.owner == self:
                logger.info(f"{self.profile_name} não é mais dono de {prop.name}.")
                prop.owner = None
        
        self.active = False


class ImpulsivePlayer(Player):
    def __init__(self):
        super().__init__()

    def _will_buy_property(self, prop):
        return super()._will_buy_property(prop)


class DemandingPlayer(Player):
    def __init__(self):
        super().__init__()

    def _will_buy_property(self, prop):
        if super()._will_buy_property(prop):
            return prop.rent_cost > 50

        return False


class CautiousPlayer(Player):
    def __init__(self):
        super().__init__()
    
    def _will_buy_property(self, prop):
        if super()._will_buy_property(prop):
            cost_with_reserve = prop.cost + 80
            return self.amount >= cost_with_reserve

        return False


class RandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def _will_buy_property(self, prop):
        if super()._will_buy_property(prop):
            return bool(random.getrandbits(1))

        return False
