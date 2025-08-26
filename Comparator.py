def rank_players_by_group_3ball(players_data):
    groups_with_rankings = []

    def convert_to_score(score):
        if score == '-':
            return float('inf')
        elif score == 'E':
            return 0
        else:
            return int(score)

    def rank_group(group):
        scores = [convert_to_score(player['Todays_Round']) for player in group]
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])
        ranks = ['first', 'second', 'third']
        final_ranks = [''] * len(group)

        for i in range(len(scores)):
            if i > 0 and scores[sorted_indices[i]] == scores[sorted_indices[i - 1]]:
                final_ranks[sorted_indices[i]] = 'tie'
                final_ranks[sorted_indices[i - 1]] = 'tie'
            else:
                final_ranks[sorted_indices[i]] = ranks[i]

        return final_ranks

    # Process players in groups of three
    for i in range(0, len(players_data), 3):
        group = players_data[i:i+3]
        if len(group) == 3:
            rankings = rank_group(group)
            group_with_rankings = [{'player': group[j], 'rank': rankings[j]} for j in range(3)]
            groups_with_rankings.append(group_with_rankings)

    return groups_with_rankings


def rank_players_by_group_2ball(players_data):
    groups_with_rankings = []

    def convert_to_score(score):
        if score == '-':
            return float('inf')  # Higher value for missing scores
        elif score == 'E':
            return 0  # "E" should be treated as 0
        else:
            return int(score)  # Convert to integer for proper sorting

    def rank_group(group):
        scores = [convert_to_score(player['Todays_Round']) for player in group]

        # Ensure sorting ranks **lower scores first**
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])  # Lower score = better rank
        ranks = ['first', 'second']
        final_ranks = [''] * len(group)

        for i in range(len(scores)):
            if i > 0 and scores[sorted_indices[i]] == scores[sorted_indices[i - 1]]:
                final_ranks[sorted_indices[i]] = 'tie'
                final_ranks[sorted_indices[i - 1]] = 'tie'
            else:
                final_ranks[sorted_indices[i]] = ranks[i]

        return final_ranks

    # Process players in groups of two
    for i in range(0, len(players_data), 2):
        group = players_data[i:i+2]
        if len(group) == 2:
            rankings = rank_group(group)
            group_with_rankings = [{'player': group[j], 'rank': rankings[j]} for j in range(2)]
            groups_with_rankings.append(group_with_rankings)

    return groups_with_rankings