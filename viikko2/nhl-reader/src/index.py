from rich import print
from rich.prompt import Prompt
from rich.table import Table
from player import PlayerReader, PlayerStats

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    season = Prompt.ask("Season", choices=["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"], default="2025-26")

    while True:
        nationality = Prompt.ask("Nationality", choices=reader.nationalities, default="")
        if nationality == "":
            break

        players = stats.top_scorers_by_nationality(nationality)

        table = Table(title=f"Season {season} players from {nationality}")

        table.add_column("Released", style="cyan", no_wrap=True)
        table.add_column("teams", style="purple")
        table.add_column("goals", style="green")
        table.add_column("assists", style="green")
        table.add_column("points", style="green")

        for player in players:
            table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))

        print(table)

if __name__ == "__main__":
    main()
