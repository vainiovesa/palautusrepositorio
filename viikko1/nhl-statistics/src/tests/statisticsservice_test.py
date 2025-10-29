import unittest
from statistics_service import StatisticsService, SortBy
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_nimi_loytyy(self):
        player = self.stats.search("Yzerman")
        self.assertEqual(player.name, "Yzerman")

    def test_nimi_ei_loydy(self):
        player = self.stats.search("Ankka")
        self.assertIsNone(player)

    def test_joukkue_loytyy(self):
        players = self.stats.team("EDM")
        players = [player.name for player in players]
        actual = ["Semenko", "Kurri", "Gretzky"]
        self.assertEqual(players, actual)

    def test_joukkue_ei_loydy(self):
        players = self.stats.team("Karhukopla")
        self.assertEqual(players, [])

    def test_top_yksi_toimii(self):
        top_players = self.stats.top(0)

        self.assertEqual(len(top_players), 1)
        self.assertEqual(top_players[0].name, "Gretzky")

    def test_top_kaikki_toimii(self):
        top_players = self.stats.top(4)

        self.assertEqual(len(top_players), 5)

        top_players = [player.name for player in top_players]
        actual = ["Gretzky", "Lemieux", "Yzerman", "Kurri", "Semenko"]

        self.assertEqual(top_players, actual)

    def test_top_kaikki_toimii(self):
        top_players = self.stats.top(4, SortBy.POINTS)

        self.assertEqual(len(top_players), 5)

        top_players = [player.name for player in top_players]
        actual = ["Gretzky", "Lemieux", "Yzerman", "Kurri", "Semenko"]

        self.assertEqual(top_players, actual)

    def test_top_kaikki_toimii_maaleilla(self):
        top_players = self.stats.top(4, SortBy.GOALS)

        self.assertEqual(len(top_players), 5)

        top_players = [player.name for player in top_players]
        actual = ["Lemieux", "Yzerman", "Kurri", "Gretzky", "Semenko"]

        self.assertEqual(top_players, actual)

    def test_top_kaikki_toimii_syotoilla(self):
        top_players = self.stats.top(4, SortBy.ASSISTS)

        self.assertEqual(len(top_players), 5)

        top_players = [player.name for player in top_players]
        actual = ["Gretzky", "Yzerman", "Lemieux", "Kurri", "Semenko"]

        self.assertEqual(top_players, actual)
