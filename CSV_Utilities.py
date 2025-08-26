import csv
import json

def write_to_csv(players_data, filename):
    if not players_data:
        print("No data to write.")
        return

    fieldnames = players_data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  
        for player in players_data:
            writer.writerow(player)
    print('CSV Updated')  


def read_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)
    
def read_tourney_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        tourney_name = lines[0].strip()
        group_size = int(lines[1].strip())
    return tourney_name, group_size

def read_csv_to_dict(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_dict_to_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
def all_players_finished(csv_file):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Position'] == 'CUT':  # Stop reading once we reach 'CUT'
                break
            if row['Through'] != 'F':  # If any player has not finished, return 0
                return 0
    return 1 

def no_players_started(csv_file):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Position'] == 'CUT':  # Stop reading once we reach 'CUT'
                break
            if row['Through'] != '-':  # If any players has started
                return 1
    return 0

def parse_grouped_with(file_path):
    players = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Grouped_With'] = json.loads(row['Grouped_With'].replace("'", '"'))
            players.append(row)
    return players

def read_original_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

