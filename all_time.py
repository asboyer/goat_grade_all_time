from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_player_stats(name, num):
    l = name.lower().split(" ")
    player_string = f"{l[1][0:5] + l[0][0:2]}0{str(num)}"
    url = f"https://www.basketball-reference.com/players/{player_string[0]}/{player_string}.html"

    r = requests.get(url)
    # html = urlopen(url)
    # soup = BeautifulSoup(html, 'html.parser')

    with open('file.html', 'w+') as file:
        file.write(r.text)

get_player_stats('Michael Jordan', 1)