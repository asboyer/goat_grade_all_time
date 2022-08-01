from get_team import get_team_players
from all_time import get_player_stats
import json
from all_players import all_players_list
# f = open('teams.json')
# data = json.load(f)
# all_players = []
# for team in data["teams"]:
#     all_players += get_team_players(team)

added_players = []


for name in all_players_list:
    num = 1
    if name in added_players:
        num = added_players.count(name) + 1
    print(name)

    s = get_player_stats(name, num)
    if s != False:
        with open("players/" + name.replace(" ", "_").lower() + str(num) + ".json", 'w+', encoding='utf-8') as file:
            file.write(json.dumps(s, indent=4, ensure_ascii=False))
        added_players.append(name)
