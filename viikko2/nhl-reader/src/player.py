import requests

class Player: # pylint: disable=too-few-public-methods
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.nationality = player_dict['nationality']
        self.team = player_dict['team']
        self.goals = player_dict['goals']
        self.assists = player_dict['assists']

    def __str__(self):
        name_team = f"{self.name:20} {self.team:15} "
        points = f"{self.goals:<2} + {self.assists:<2} = {self.goals + self.assists}"
        return name_team + points

class PlayerReader: # pylint: disable=too-few-public-methods
    def __init__(self, url):
        response = requests.get(url, timeout=10).json()
        nationalities = set()

        self.players = []

        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)
            nationalities.add(player.nationality)

        self.nationalities = list(nationalities)

class PlayerStats: # pylint: disable=too-few-public-methods
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        top = []
        for player in sorted(self.reader.players, key=lambda x: x.goals + x.assists, reverse=True):
            if player.nationality == nationality:
                top.append(player)
        return top
