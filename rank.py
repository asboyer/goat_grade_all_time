import json

with open('stats.json', 'r', encoding='utf8') as file:
    stats = json.load(file)

ranks = {}
for player in stats:
    ranks[player] = {}

categories = ['MP', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'PTS', 'FG%', '3P%', 'FT%', 'MP_PG', 'PTS_PG', 'RB_PG', 'AST_PG']

def rank(category):
    category_rankings = []
    for player in stats:
        if stats[player][category] != "":
            category_rankings.append([player, float(stats[player][category])])
        else:
            category_rankings.append([player, 0])
    category_rankings = sorted(category_rankings, key=lambda x: x[1])
    category_rankings.reverse()

    for i in range(len(category_rankings)):
        name = category_rankings[i][0]
        value = category_rankings[i][1]
        ranks[name][f'{category}_rank'] = i + 1
        # ranks[name][category] = value

for category in categories:
    rank(category)

for player in ranks:
    score = 0
    for category in ranks[player]:
        score += ranks[player][category]
    ranks[player]['grade'] = score

final_ranks = []
for player in ranks:
    final_ranks.append([player, int(ranks[player]['grade'])])
final_ranks = sorted(final_ranks, key=lambda x: x[1])

for i in range(len(final_ranks)):
    print(str(i + 1) + ". " + final_ranks[i][0])

with open('ranks.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(ranks, ensure_ascii=False, indent =4))