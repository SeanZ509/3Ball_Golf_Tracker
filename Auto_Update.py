import schedule
import time
from datetime import datetime
import threading
import os
import shutil
from Updates.Update_Scores import update_player_scores
from Updates.Schedule import makeRoundTab, is_tournament_complete
from Utilities.CSV_Utilities import all_players_finished
from Utilities.Scans import Initial_Scan

# 🔹 Function to auto-update scores
def run_script():
    update_player_scores('https://www.pgatour.com/leaderboard', True)

# 🔹 Function to re-scan groups
def run_rescan_groups():
    Initial_Scan('https://www.pgatour.com/leaderboard')

# 🔹 Check and update schedule dynamically
def check_and_update_schedule():
    now = datetime.now()
    current_day = now.strftime('%A')
    current_hour = now.hour

    # 🔥 Stop updates if Round 4 is finished AND lock file exists
    if is_tournament_complete():
        print("✅ Tournament is complete. Auto-updates are permanently stopped.")
        schedule.clear()  # Stop all scheduled tasks
        return  # Exit the function early

    # Normal operation: Continue updating during tournament
    if current_day in ['Thursday', 'Friday', 'Saturday', 'Sunday'] and 5 <= current_hour < 23:
        if all_players_finished('CSV/pga_leaderboard.csv') == 0:
            schedule.every(5).minutes.do(run_script)
        else:
            makeRoundTab()  # 🔥 Creates results only once
            schedule.clear()
    else:
        schedule.clear()

# 🔹 Runs rescan every Friday and Saturday at 10 PM
def schedule_weekend_tasks():
    schedule.every().thursday.at("22:00").do(run_rescan_groups)
    schedule.every().friday.at("22:00").do(run_rescan_groups)
    schedule.every().saturday.at("22:00").do(run_rescan_groups)

# 🔹 Background task to keep auto-updating
def auto_update_task():
    schedule_weekend_tasks()
    while True:
        check_and_update_schedule()
        schedule.run_pending()
        time.sleep(60)  # 🔥 Runs every minute

# 🔹 Starts auto-update thread
def start_auto_update():
    threading.Thread(target=auto_update_task, daemon=True).start()