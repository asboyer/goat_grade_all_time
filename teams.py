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
    file.write(teams)