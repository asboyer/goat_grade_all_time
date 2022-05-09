from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def text(raw):
    t = raw.getText().strip().replace("\n", "")
    while "  " in t:
        t = t.replace("  ", " ")
    return t

def get_player_stats(name, num):
    l = name.lower().split(" ")
    player_string = f"{l[1][0:5] + l[0][0:2]}0{str(num)}"
    url = f"https://www.basketball-reference.com/players/{player_string[0]}/{player_string}.html"

    r = requests.get(url)
    try:
        html = urlopen(url)
    except:
        print('player not found')
        return
    soup = BeautifulSoup(html, 'html.parser')

    with open('file.html', 'w+') as file:
        file.write(r.text)

    stats = {}

    ps = soup.findAll('p')[0:3]
    for p in range(len(ps)):

        t = text(ps[p])

        if p == 0 and "pronunciation" in t.lower():
            t = text(ps[p + 1])
        if p == 0 and "▪" not in t.lower():
            stats['name'] = t
        elif p == 0:
            ats = t.split(" ▪ ")
            stats['name'] = ats[0].split(": ")
            if 'twitter' in t.lower() and 'instagram' in t.lower():
                stats['twitter'] = ats[1].split(": ")[1]
                stats['instagram'] = ats[2].split(": ")[1]
            if 'twitter' in t.lower() and 'instagram' not in t.lower():
                stats['twitter'] = ats[1].split(": ")[1]
            if 'instagram' in t.lower() and 'twitter' not in t.lower():
                stats['instagram'] = ats[1].split(": ")[1]
        if (p == 1 or p == 2) and '(born' in t.lower():
            stats['former_name'] = t.split("(born ")[1].replace(")", "")
        if (p == 1 or p == 2 or p == 3) and '(' in t.lower() and '(born' not in t.lower():
            stats['nicknames'] = t.replace("(", "").replace(")", "").split(", ")
    return stats

name = 'Michael Jordan'
s = get_player_stats(name, 1)
with open("players/" + name.replace(" ", "_").lower() + ".json", 'w+') as file:
    file.write(json.dumps(s, indent=4, ensure_ascii=False))