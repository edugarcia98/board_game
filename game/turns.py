from random import shuffle, choice

from game.board import create_board
from logger import logger
from flows import PlayerFlow
from schemas import (
    CautiousPlayer,
    DemandingPlayer,
    ImpulsivePlayer,
    RandomPlayer,
)

DIE = list(range(1, 7))


def _initialize_players():
    cautious_player = CautiousPlayer()
    demanding_player = DemandingPlayer()
    impulsive_player = ImpulsivePlayer()
    random_player = RandomPlayer()

    players = [cautious_player, demanding_player, impulsive_player, random_player]
    shuffle(players)

    return players


def _game_round(players, **board_info):
    for player in players:
        params = {"player": player, "spaces": choice(DIE), **board_info}

        player_flow = PlayerFlow(**params)
        result = player_flow.execute()

        logger.info("\n")


def _get_winner_when_timeout(players):
    higher_amount = max([player.amount for player in players])
    winner = [player for player in players if player.amount == higher_amount][0]

    logger.info(f"{winner.profile_name} é o vencedor.")

    return winner.profile_name


def full_game(game_number):
    logger.info(f"Iniciando jogo {game_number}")

    game_metrics = {
        "winner": None,
        "turns": None,
        "timeout": False,
    }

    board = create_board()
    board_info = {
        "board": board,
        "board_size": len(board),
        "board_max_idx": len(board) - 1,
    }

    winner = None
    players = _initialize_players()

    for turn in range(1, 1001):
        logger.info(f"Iniciando turno {turn}\n")

        _game_round(players, **board_info)
        [players.remove(player) for player in players if not player.active]

        if len(players) == 1:
            winner = players[0]
            logger.info(f"{winner.profile_name} é o vencedor.")

            game_metrics["winner"] = winner.profile_name
            game_metrics["turns"] = turn

            break
    else:
        logger.info("Empate! Validando jogador com mais saldo.")
        
        game_metrics["winner"] = _get_winner_when_timeout(players)
        game_metrics["turns"] = turn
        game_metrics["timeout"] = True

    return game_metrics
