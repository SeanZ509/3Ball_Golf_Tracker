from flask import Flask, render_template, jsonify, request
import Utilities.Comparator
import Utilities.CSV_Utilities
import Utilities.Scans
import Updates.Schedule
import os
from Updates.Auto_Update import start_auto_update

app = Flask(__name__)

@app.route('/')
def index():
    key = request.args.get('key', 'Group_Leaderboard')  # Default to Group Leaderboard
    group_data = Utilities.CSV_Utilities.read_csv('CSV/sorted_pga_leaderboard.csv')
    solo_data = Utilities.CSV_Utilities.read_csv('CSV/pga_leaderboard.csv')
    grouped_with = Utilities.CSV_Utilities.parse_grouped_with('CSV/pga_leaderboard.csv')
    TOURNEY_NAME, GROUP_SIZE = Utilities.CSV_Utilities.read_tourney_info('Tourney_Info.txt')
    print(GROUP_SIZE)

    # 🔹 Get current day of the tournament
    day_of_week = Updates.Schedule.get_day_of_week()
    round = ""
    
    if day_of_week == 1:
        ROUND_STATUS = 'Round 1 Not Started'
    elif day_of_week == 3:
        round = 'Round 1'
    elif day_of_week == 4:
        round = 'Round 2'
    elif day_of_week == 5:
        round = 'Round 3'
    elif day_of_week == 6:
        round = 'Round 4'

    # 🔹 Determine if round is ongoing or complete
    if day_of_week != 1:  # Skip for Monday-Wednesday
        if Utilities.CSV_Utilities.all_players_finished('CSV/pga_leaderboard.csv') == 0:
            ROUND_STATUS = round + ' Ongoing'
        else:
            ROUND_STATUS = round + ' Complete'

    # 🔹 Pass results availability for disabling buttons in the UI
    results_available = {
        'R1': os.path.exists('CSV/R1_Results.csv'),
        'R2': os.path.exists('CSV/R2_Results.csv'),
        'R3': os.path.exists('CSV/R3_Results.csv'),
        'R4': os.path.exists('CSV/R4_Results.csv'),
    }

    # 🔹 Load appropriate leaderboard based on group size
    if key == 'Group_Leaderboard':
        if GROUP_SIZE == 3:
            group_placement = Utilities.Comparator.rank_players_by_group_3ball(group_data)
            return render_template('index3Ball.html', group_placement=group_placement, TOURNEY_NAME=TOURNEY_NAME, ROUND_STATUS=ROUND_STATUS, grouped_with=grouped_with, results_available=results_available)
        else:
            group_placement = Utilities.Comparator.rank_players_by_group_2ball(group_data)
            return render_template('index2Ball.html', group_placement=group_placement, TOURNEY_NAME=TOURNEY_NAME, ROUND_STATUS=ROUND_STATUS, grouped_with=grouped_with, results_available=results_available)

    elif key == 'Solo':
        return render_template('indexSolo.html', solo_data=solo_data, TOURNEY_NAME=TOURNEY_NAME, ROUND_STATUS=ROUND_STATUS, results_available=results_available)

    # 🔹 Load round results only if they exist
    elif key in ['R1', 'R2', 'R3', 'R4']:
        result_file = f'CSV/{key}_Results.csv'
        if not results_available[key]:  # 🔥 Simplified existence check
            return "Not Active, Round Not Complete Yet"
        else:
            result_data = Utilities.CSV_Utilities.read_csv(result_file)
            if key in ['R1', 'R2']:
                group_placement = Utilities.Comparator.rank_players_by_group_3ball(result_data)
            else:
                group_placement = Utilities.Comparator.rank_players_by_group_2ball(result_data)

            return render_template(f'index{key}Results.html', group_placement=group_placement, TOURNEY_NAME=TOURNEY_NAME, results_available=results_available)

@app.route('/api/players')
def get_players():
    players_data = Utilities.CSV_Utilities.read_csv('CSV/sorted_pga_leaderboard.csv')  # 🔹 Ensure correct path
    return jsonify(players_data)

if __name__ == '__main__':
    start_auto_update() 
    app.run(debug=True)