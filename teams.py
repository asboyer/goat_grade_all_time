from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


url = f"https://www.basketball-reference.com/teams/"

r = requests.get(url)
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

with open('file1.html', 'w+') as file:
    file.write(r.text)

teams_div = soup.findAll('th', {'data-stat': 'franch_name'})
print(teams_div)
with open('test.txt', 'w+') as file:
    for team in teams_div:
        file.write(str(team))
        file.write("\n__________________\n")

teams = []
for team in teams_div:
    teams.append(str(team))
with open('test1.txt', 'w+') as file:
    for team in teams:
        file.write(team)
        file.write("\n__________________\n")

stop_index = 0
header_str = teams.pop(0)
for i in range(len(teams)):
    if teams[i] == header_str:
        stop_index = i
        break
teams = teams[0:i]

new_teams = []
for team in teams:
    soup1 = BeautifulSoup(team, 'html.parser')
    new_teams.append(soup1.findAll('a')[0]['href'].split("/")[2])

with open('test1.txt', 'w+') as file:
    for team in new_teams:
        file.write(team)
        file.write("\n__________________\n")

s = {
    "teams": new_teams
}

with open('teams.json', 'w+') as file:
    file.write(json.dumps(s, indent=4, ensure_ascii=False))

