from logger import logger
from schemas import Player


class PlayerFlow:
    def __init__(self, player: Player, spaces: int, **board_info):
        self.player = player
        self.spaces = spaces
        self.property = None
        self.board = board_info["board"]
        self.board_size = board_info["board_size"]
        self.board_max_idx = board_info["board_max_idx"]
    
    def execute(self):
        self._move_spaces()
        self._player_action()
        self._check_player_amount()
    
    def _move_spaces(self):
        logger.info(f"{self.player.profile_name} tirou {self.spaces} no dado.")

        next_position = self.player.position + self.spaces

        if next_position > self.board_max_idx:
            next_position -= self.board_size

            logger.info(f"{self.player.profile_name} deu uma volta no tabuleiro.")
            self.player.amount += 100
        
        self.property = self.board[next_position]

        logger.info(f"{self.player.profile_name} caiu em {self.property.name}.")
    
    def _player_action(self):
        # Buy property or pay rent

        if not self.property.owner:
            logger.info(f"{self.property.name} não possui dono.")
            self.player.buy_property(self.property)
            return
        
        if self.property.owner == self.player:
            logger.info(f"{self.player.profile_name} já é o dono de {self.property.name}.")
        else:
            logger.info(
                f"{self.property.owner.profile_name} é o dono de {self.property.name}. "
                f"{self.player.profile_name} deve pagar aluguel."
            )
            self.player.pay_rent(self.property)
    
    def _check_player_amount(self):
        if self.player.amount < 0:
            logger.info(
                f"{self.player.profile_name} está com saldo negativo, "
                f"então está desclassificado."
            )
            self.player.invalidate(self.board)
