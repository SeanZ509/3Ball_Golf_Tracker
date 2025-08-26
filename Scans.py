from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import Utilities.Scraping_Utilities
import Utilities.CSV_Utilities
import Utilities.Group_Utilities
import re
import time


def Initial_Scan(URL):
    driver = Utilities.Scraping_Utilities.fetch_webpage(URL)
    TOURNEY_NAME = driver.find_element(By.TAG_NAME, 'h1').text
    leaderboard_container = driver.find_elements(By.CSS_SELECTOR, '[data-cy="leaderboard-item"]')
    players_data = Utilities.Scraping_Utilities.parse_players(leaderboard_container)
    players_data = Utilities.Scraping_Utilities.remove_duplicates(players_data)
    #group_data, GROUP_SIZE = Utilities.Group_Utilities.group_players(driver)
    driver.quit()

    #players_data_grouped = Utilities.Group_Utilities.add_group_info(players_data, group_data, GROUP_SIZE)
    #Utilities.CSV_Utilities.write_to_csv(players_data_grouped, 'CSV/pga_leaderboard.csv')

    #grouped_players = Utilities.Group_Utilities.sort_by_group(players_data_grouped)
    #Utilities.CSV_Utilities.write_to_csv(grouped_players, 'CSV/sorted_pga_leaderboard.csv')

    #with open('Tourney_Info.txt', 'w') as file:
        #.write(f"{TOURNEY_NAME}\n{GROUP_SIZE}\n")
    
    #return GROUP_SIZE, TOURNEY_NAME

def get_first_tournament_url():
    driver = webdriver.Edge()
    driver.get("https://www.google.com")

    # Accept cookies if needed (can fail silently)
    try:
        consent = driver.find_element(By.XPATH, '//button[contains(text(), "I agree")]')
        consent.click()
        time.sleep(1)
    except:
        pass  # No consent dialog, continue

    # Type in the search box
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("site:pgatour.com leaderboard")
    search_box.submit()
    time.sleep(2)

    # Get the first search result
    try:
        first_result = driver.find_element(By.XPATH, '//div[@class="g"]//a')
        leaderboard_url = first_result.get_attribute("href")
        print("✅ Found leaderboard URL:", leaderboard_url)
        driver.quit()
        return leaderboard_url
    except Exception as e:
        print("❌ Failed to get first result:", e)
        driver.quit()
        return None
    