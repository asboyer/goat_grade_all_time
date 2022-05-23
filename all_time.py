from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def text(raw):
    if 'span class="desc"' in str(raw):
        t = raw.getText().strip().replace("\n", "")
        while "  " in t:
            t = t.replace("  ", " ")
        return t + "<i>"
    else:
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
        return False
    soup = BeautifulSoup(html, 'html.parser')

    with open('file.html', 'w+') as file:
        file.write(r.text)

    stats = {}

    ps = soup.findAll('p')
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
        if (p == 1 or p == 2) and '<i>' in t.lower():
            stats['former_name'] = t.split("<i>")[0].replace(")", "").replace("(", "")
        if (p in list(range(0, 5))) and t.lower()[0] == '(' and '<i>' not in t.lower() and t[1] != '-':
            stats['nicknames'] = t.replace("(", "").replace(")", "").split(", ")
        if p in list(range(0, 6)) and 'position: ' in t.lower():
            stats['position'] = t.lower().split('position: ')[1].split(' ▪')[0]
            stats['shooting_hand'] = t.lower().split('shoots: ')[1]
        if p in list(range(1, 10)) and t[1] == '-':
            stats['height'] = t.split(',')[0]
            stats['weight'] = t.split(',')[1].split('lb')[0].strip()
        if p in list(range(2, 11)) and t.lower()[0:6] == 'born: ':
            stats['birthday'] = (t.lower().split('born')[1].split(' in')[0])[2:]
            stats['birthplace'] = t.lower().split('in ')[1].replace(', ', ', ')[0:-2] + " " + t.lower()[len(t)-2:len(t)].upper()
        if p in list(range(2, 12)) and t.lower()[0:6] == 'died: ':
            stats['died'] = (t.lower().split('died')[1].split('(')[0])[2:].replace(' ', ' ')
        if p in list(range(2, 14)) and (t.lower()[0:9] == 'college: ' or t.lower()[0:10] == 'colleges: '):
            if 'college: ' in t.lower():
                stats['college'] = t.lower().split('college:')[1][1:]
            if 'colleges: ' in t.lower():
                stats['colleges'] = t.lower().split('colleges:')[1][1:].split(', ')
    return stats

name = 'duncan robinson'
s = get_player_stats(name, 1)
if s != False:
    with open("players/" + name.replace(" ", "_").lower() + ".json", 'w+', encoding='utf-8') as file:
        file.write(json.dumps(s, indent=4, ensure_ascii=False))