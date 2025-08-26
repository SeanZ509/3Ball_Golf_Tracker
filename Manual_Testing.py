import Utilities.Scans
#import Updates.Update_Scores

LEADERBOARD_URL = 'https://www.pgatour.com/leaderboard'

GROUP_SIZE, TOURNEY_NAME = Utilities.Scans.Initial_Scan(LEADERBOARD_URL) #Works!!
#Updates.Update_Scores.update_player_scores(LEADERBOARD_URL, roundStarted=False) #Should Work
