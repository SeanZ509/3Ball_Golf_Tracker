import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import Utilities.Scraping_Utilities
import Updates.Schedule


def group_players(driver):
    # Wait for the tab container to load
    time.sleep(3)

    try:
        # Find the <a> tag inside the button with aria-label="Tee Times"
        tee_times_link = driver.find_element(By.XPATH, '//a[@aria-label="Tee Times"]')
        href = tee_times_link.get_attribute("href")
        if not href:
            print("❌ Tee Times link does not have a href")
            return [], 3
        
        print(f"🔗 Navigating to Tee Times URL: {href}")
        driver.get(href)

    except NoSuchElementException:
        print("❌ Could not find the Tee Times <a> link")
        return [], 3

    # Wait for the tee times table to load
    time.sleep(3)

    try:
        table = driver.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        NUM_GROUPS = len(rows)
    except Exception as e:
        print(f"❌ Could not locate tee times table: {e}")
        return [], 3

    # Determine group size based on day
    key = Updates.Schedule.get_day_of_week()
    GROUP_SIZE = 2 if key in [5, 6] else 3

    group_data = Utilities.Scraping_Utilities.parse_groups(driver, NUM_GROUPS - 1, GROUP_SIZE)
    driver.quit()
    return group_data, GROUP_SIZE

def parse_groups(driver, group_size=3):
    groups = []
    try:
        rows = driver.find_elements(By.XPATH, "//table//tbody//tr")
        for row in rows:
            try:
                player_spans = row.find_elements(By.CSS_SELECTOR, "td:nth-child(3) span.chakra-text")
                players = [span.text.strip() for span in player_spans if span.text.strip()]

                if len(players) == group_size:
                    if group_size == 3:
                        groups.append({
                            'Golfer_One': players[0],
                            'Golfer_Two': players[1],
                            'Golfer_Three': players[2],
                        })
                    elif group_size == 2:
                        groups.append({
                            'Golfer_One': players[0],
                            'Golfer_Two': players[1],
                        })
            except Exception as e:
                print(f"Error parsing group row: {e}")
                continue

        print(f"✅ Parsed {len(groups)} groups from tee times page.")
        return groups
    except Exception as e:
        print(f"❌ Error finding group rows: {e}")
        return []

def add_group_info(players_data, group_data, GROUP_SIZE):
    grouped_with_dict = {}

    for group in group_data:
        players = list(group.values())
        for player in players:
            if player not in grouped_with_dict:
                grouped_with_dict[player] = set()
            grouped_with_dict[player].update(p for p in players if p != player)

    for player in players_data:
        player_name = player['Player']
        player['Grouped_With'] = list(grouped_with_dict.get(player_name, []))

    return players_data

def sort_by_group(players_data):
    grouped_data = []
    seen_players = set()
    player_to_group = {}

    def convert_position(pos):
        if pos.startswith("T"):
            return int(pos[1:])
        elif pos in ['CUT', 'WD', 'N/A']:
            return 99
        return int(pos)

    for player in players_data:
        grouped_with = player['Grouped_With']
        if grouped_with != 'N/A':
            if player['Player'] not in player_to_group:
                player_to_group[player['Player']] = set()
            for group_member in grouped_with:
                if group_member not in player_to_group:
                    player_to_group[group_member] = set()
                player_to_group[player['Player']].add(group_member)
                player_to_group[group_member].add(player['Player'])

    for player in players_data:
        if player['Player'] not in seen_players:
            group = [player]
            seen_players.add(player['Player'])
            for grouped_player_name in player_to_group.get(player['Player'], []):
                for grouped_player in players_data:
                    if grouped_player['Player'] == grouped_player_name and grouped_player['Player'] not in seen_players:
                        group.append(grouped_player)
                        seen_players.add(grouped_player['Player'])

            group_sorted_by_position = sorted(group, key=lambda x: convert_position(x['Position']))
            grouped_data.extend(group_sorted_by_position)

    return grouped_data
