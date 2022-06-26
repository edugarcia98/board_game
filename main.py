import pandas as pd

from game import full_game
from logger import logger


results = [full_game(i) for i in range(1, 301)]

df = pd.DataFrame(results)

logger.info("\nMÉTRICAS:\n")

timeout_games = len(df[df["timeout"]])
mean_turns = df["turns"].mean()
wins_by_profile = df["winner"].value_counts()
most_winner = wins_by_profile.idxmax()

logger.info(f"Partidas que terminaram por timeout: {timeout_games}.\n")
logger.info(f"Média de turnos que demora uma partida: {mean_turns:.0f}.\n")

for profile in wins_by_profile.index:
    pct = (wins_by_profile[profile] / len(df)) * 100

    logger.info(f"Porcentagem de vitórias para {profile}: {pct:.2f}%.")

logger.info(f"\nComportamento que mais vence: {most_winner}.")