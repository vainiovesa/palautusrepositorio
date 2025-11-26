class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name

        self.player_scores = {player1_name: 0, player2_name: 0}

    def won_point(self, player_name):
        self.player_scores[player_name] += 1

    def get_score(self):
        deuce_threshold = 3
        player1_score = self.player_scores[self.player1_name]
        player2_score = self.player_scores[self.player2_name]

        if player1_score == player2_score:
            score_str = self._scores_equal(player1_score)
        elif player1_score > deuce_threshold or player2_score > deuce_threshold:
            score_str = self._players_score_over_limit(player1_score, player2_score)
        else:
            score_str = self._scores_under_limit(player1_score, player2_score)

        return score_str

    def _scores_equal(self, player_score):
        scores = ["Love-All", "Fifteen-All", "Thirty-All", "Deuce"]
        if player_score < 4:
            score_str = scores[player_score]
        else:
            score_str = scores[-1]
        return score_str

    def _players_score_over_limit(self, player1_score, player2_score):
        diff = player1_score - player2_score

        if diff == 1:
            score_str = "Advantage player1"
        elif diff == -1:
            score_str = "Advantage player2"
        elif diff >= 2:
            score_str = "Win for player1"
        else:
            score_str = "Win for player2"
        return score_str

    def _scores_under_limit(self, player1_score, player2_score):
        scores = ["Love", "Fifteen", "Thirty", "Forty"]
        score_str = scores[player1_score] + "-" + scores[player2_score]

        return score_str
