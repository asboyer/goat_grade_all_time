from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_team_stats(team):
    url = f"https://www.basketball-reference.com/teams/{team.upper()}/players.html"
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.findAll('tr')

    # with open('file.txt', 'w+') as file:
    #     for row in rows:
    #         file.write(str(row))
    #         file.write("\n\n\n")

    headers = []
    hs = rows[1].findAll('th')
    for h in hs:
        headers.append(h.getText())
    headers = headers[1:]
    headers[-1] = 'AST_PG'
    headers[-2] = 'RB_PG'
    headers[-3] = 'PTS_PG'
    headers[-4] = 'MP_PG'

    # print(headers)
    rs = []
    for row in rows:
        if 'aria-label' in str(row):
            pass
        else:
            rs.append(row)

    # with open('file.txt', 'w+') as file:
    #     for row in rs:
    #         file.write(str(row))
    #         file.write("\n\n\n")

    stats = {}

    for i in range(len(rs)):
        tds = rs[i].findAll("td")
        h = 0
        name = tds[0].getText()
        stats[name] = {}
        for td in tds:
            stats[name][headers[h]] = td.getText()
            h += 1
    with open('stats.json', 'w+') as file:
        file.write(json.dumps(stats, indent=4, ensure_ascii=False))
get_team_stats('OKC')