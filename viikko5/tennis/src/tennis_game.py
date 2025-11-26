class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name

        self.player_scores = {player1_name: 0, player2_name: 0}

    def won_point(self, player_name):
        self.player_scores[player_name] += 1

    def get_score(self):
        score = ""
        temp_score = 0

        player1_score = self.player_scores[self.player1_name]
        player2_score = self.player_scores[self.player2_name]

        if player1_score == player2_score:
            scores = ["Love-All", "Fifteen-All", "Thirty-All", "Deuce"]
            if player1_score < 4:
                score = scores[player1_score]
            else:
                score = scores[-1]

        elif player1_score >= 4 or player2_score >= 4:
            minus_result = player1_score - player2_score

            if minus_result == 1:
                score = "Advantage player1"
            elif minus_result == -1:
                score = "Advantage player2"
            elif minus_result >= 2:
                score = "Win for player1"
            else:
                score = "Win for player2"
        else:
            scores = ["Love", "Fifteen", "Thirty", "Forty"]
            for i in range(1, 3):
                if i == 1:
                    temp_score = player1_score
                else:
                    score = score + "-"
                    temp_score = player2_score

                score = score + scores[temp_score]

        return score


