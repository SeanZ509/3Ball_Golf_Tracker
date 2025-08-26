import Utilities.CSV_Utilities
import Utilities.Scraping_Utilities

def update_player_scores(LEADERBOARD_URL, roundStarted):
    driver = Utilities.Scraping_Utilities.fetch_webpage(LEADERBOARD_URL)
    players_data = Utilities.Scraping_Utilities.parse_players(driver, roundStarted)
    Utilities.CSV_Utilities.write_to_csv(players_data, 'CSV/pga_leaderboard.csv')
    update_grouped_leaderboard_csv()
    
    
def update_grouped_leaderboard_csv():
    players_data = Utilities.CSV_Utilities.read_csv('CSV/pga_leaderboard.csv')
    player_scores = {player['Player']: player for player in players_data}
    group_players_data = Utilities.CSV_Utilities.read_csv('CSV/sorted_pga_leaderboard.csv')
    

    for group_player in group_players_data:
        player_name = group_player['Player']
        if player_name in player_scores:
            group_player['Position'] = player_scores[player_name]['Position']
            group_player['Score'] = player_scores[player_name]['Score']
            group_player['Through'] = player_scores[player_name]['Through']
            group_player['Todays_Round'] = player_scores[player_name]['Todays_Round']
            group_player['R1'] = player_scores[player_name]['R1']
            group_player['R2'] = player_scores[player_name]['R2']
            group_player['R3'] = player_scores[player_name]['R3']
            group_player['R4'] = player_scores[player_name]['R4']

    Utilities.CSV_Utilities.write_to_csv(group_players_data, 'CSV/sorted_pga_leaderboard.csv')