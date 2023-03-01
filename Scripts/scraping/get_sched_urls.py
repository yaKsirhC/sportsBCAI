import bs4.element
import requests
from bs4 import BeautifulSoup

def get_sched_urls():
    url = 'https://basketball.realgm.com/international/league/1/Euroleague/team/142/ALBA-Berlin/schedule'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    teams = soup.find('div', id='teamnav').findAll('a', href=True)
    # print(type(teams))
    allteams = []
    for team in teams:
        if isinstance(team, bs4.element.Tag):
            team_name = str(team['href']).split('/')[-1]
            team_sched_url = "https://basketball.realgm.com/" + team['href'] + "/schedule/"
            allteams.append([team_name, team_sched_url])
    return allteams
