from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from Updates.Schedule import get_day_of_week

def fetch_webpage(url):
    service = Service(r'C:\Users\seanz\WD\msedgedriver.exe')  
    options = webdriver.EdgeOptions()

    # Use headless mode if necessary
    options.add_argument('--headless=new')  # new headless mode for better compatibility
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    # Spoof real browser user-agent to avoid CloudFront block
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)
    return driver


def parse_players(driver):
    try:
        players_data = []
        player_elements = driver.find_elements(By.CSS_SELECTOR, '[data-cy="leaderboard-item"]')

        for player in player_elements:
            try:
                pos_elem = player.find_element(By.CSS_SELECTOR, '[aria-label^="position"]')
                name_elem = player.find_element(By.CSS_SELECTOR, '[data-cy="item-name"]')
                score_elem = player.find_element(By.CSS_SELECTOR, '[aria-label^="total score"]')
                thru_elem = player.find_element(By.CSS_SELECTOR, '[aria-label^="through"]')

                # Try to extract round scores dynamically
                def get_round_score(prefix):
                    try:
                        elem = player.find_element(By.CSS_SELECTOR, f'[aria-label^="{prefix}"]')
                        return elem.text.strip()
                    except:
                        return ''

                r1 = get_round_score("first round score")
                r2 = get_round_score("second round score")
                r3 = get_round_score("third round score")
                r4 = get_round_score("fourth round score")

                player_data = {
                    'Position': pos_elem.get_attribute('aria-label').replace('position: ', '').strip(),
                    'Player': name_elem.get_attribute('data-gtm-player-name').strip(),
                    'Score': score_elem.get_attribute('aria-label').replace('total score: ', '').strip(),
                    'Through': thru_elem.get_attribute('aria-label').replace('through ', '').strip(),
                    'Todays_Round': r1 if r1 else r2 if r2 else r3 if r3 else r4,
                    'R1': r1,
                    'R2': r2,
                    'R3': r3,
                    'R4': r4
                }

                players_data.append(player_data)
            except Exception as inner_e:
                print(f"Skipping player due to error: {inner_e}")

        return players_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def parse_groups(driver, NUM_GROUPS, GROUP_SIZE):
    try:
        group_data = []
        for i in range(1,NUM_GROUPS):
                row = driver.find_element(By.XPATH, '//tbody/tr[' + str(i) + ']')
                row_text = row.text
                lines = row_text.splitlines()
                if len(lines) == 0:
                        None
                else:
                    if GROUP_SIZE == 2:
                        p1 = lines[3].strip()
                        p2 = lines[4].strip()

                        group_data.append({
                                    'Golfer_One': p1,
                                    'Golfer_Two': p2
                        })
                    else:
                        p1 = lines[3].strip()
                        p2 = lines[4].strip()
                        p3 = lines[5].strip()

                        group_data.append({
                                    'Golfer_One': p1,
                                    'Golfer_Two': p2,
                                    'Golfer_Three': p3
                        })
        driver.close()
        return group_data 
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def remove_duplicates(players_data):
    seen = set()
    unique_players = []
    for player in players_data:
        player_name = player['Player']
        if player_name not in seen:
            seen.add(player_name)
            unique_players.append(player)
    return unique_players