import requests

class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.team = dict['team']
        self.goals = dict['goals']
        self.assists = dict['assists']

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:<2} + {self.assists:<2} = {self.goals + self.assists}"

class PlayerReader:
    def __init__(self, url):
        response = requests.get(url).json()
        nationalities = set()

        self.players = []

        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)
            nationalities.add(player.nationality)

        self.nationalities = list(nationalities)

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        top = []
        for player in sorted(self.reader.players, key=lambda x: x.goals + x.assists, reverse=True):
            if player.nationality == nationality:
                top.append(player)
        return top