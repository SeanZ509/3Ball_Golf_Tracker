from datetime import datetime
import Utilities.CSV_Utilities
import shutil
import os
import schedule

# 🔹 Path to lock file
TOURNAMENT_COMPLETE_FILE = "CSV/.tournament_complete"

def get_day_of_week():
    today = datetime.today().weekday()  # Monday=0, Sunday=6
    return today if today in [3, 4, 5, 6] else 1  # Default to Thursday (3)

def makeRoundTab():
    key = Utilities.CSV_Utilities.all_players_finished('CSV/pga_leaderboard.csv')
    today = get_day_of_week()
    
    round_mapping = {3: "R1", 4: "R2", 5: "R3", 6: "R4"}
    
    if today in round_mapping and key == 1:
        round_file = f'CSV/{round_mapping[today]}_Results.csv'
        
        # 🔹 Ensure this only runs ONCE per round
        if not os.path.exists(round_file):  
            shutil.copy('CSV/sorted_pga_leaderboard.csv', round_file)
            print(f'✅ Created {round_mapping[today]}_Results.csv')

            # 🔥 If Round 4 is complete, STOP AUTO UPDATES & CREATE LOCK FILE
            if today == 6:
                print("✅ Round 4 Complete. Stopping all auto-updates.")
                with open(TOURNAMENT_COMPLETE_FILE, 'w') as f:
                    f.write("Tournament Complete")  # Creates lock file
                schedule.clear()  # Stop auto updates
                save_tournament_results()
                schedule_deletion_next_wednesday()
        else:
            print(f'⏳ {round_mapping[today]}_Results.csv already exists. No duplicate creation.')

# 🔹 Check if tournament has already been marked complete
def is_tournament_complete():
    return os.path.exists(TOURNAMENT_COMPLETE_FILE)

# 🔹 Saves the last 5 tournaments
def save_tournament_results():
    tournament_dir = 'CSV/Tournament_Results/'
    if not os.path.exists(tournament_dir):
        os.makedirs(tournament_dir)

    tournament_files = sorted(
        [f for f in os.listdir(tournament_dir) if f.endswith('.csv')],
        key=lambda x: os.path.getmtime(os.path.join(tournament_dir, x))
    )

    # Keep only the last 5 tournaments
    while len(tournament_files) > 5:
        os.remove(os.path.join(tournament_dir, tournament_files.pop(0)))

# 🔹 Deletes old tournament CSVs the following Wednesday
def schedule_deletion_next_wednesday():
    schedule.every().wednesday.at("04:00").do(delete_old_csvs)

def delete_old_csvs():
    print("🗑️ Deleting old tournament CSV files...")

    csv_files = [
        'CSV/pga_leaderboard.csv', 
        'CSV/sorted_pga_leaderboard.csv', 
        'CSV/R1_Results.csv', 
        'CSV/R2_Results.csv', 
        'CSV/R3_Results.csv', 
        'CSV/R4_Results.csv'
    ]
    
    for file in csv_files:
        if os.path.exists(file):
            os.remove(file)
            print(f'🗑️ Deleted {file}')
    
    # 🔹 Also delete the lock file so next tournament works as expected
    if os.path.exists(TOURNAMENT_COMPLETE_FILE):
        os.remove(TOURNAMENT_COMPLETE_FILE)
    
    print("✅ All old tournament files removed.")