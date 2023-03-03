import bs4.element
import requests
from bs4 import BeautifulSoup
import sqlite_operations as sqlo
from timer import py_timer
from data_converter import allpd_parser


def m_url_sco_map(row):
    if isinstance(row, bs4.element.Tag):
        d = row.find('td').findNextSibling('td').findNextSibling('td').find('a')
        if d is None:
            return
        match_url = "https://basketball.realgm.com/" + d['href']
        match_score = d.text
        return [match_url, match_score]

def get_match_score(soup, score_num):
    try:
        match_score_soup = soup.find('h2', style='line-height: 2em; margin-top: 1em;').find('a')
        home_name_score = [match_score_soup.text, score_num[3:].split('-')[0].strip()]
        away_name_score = [match_score_soup.findNext('a').text, score_num[3:].split('-')[1].strip()]
        return [home_name_score, away_name_score]
    except AttributeError:
        # print(soup)
        return 

def worker(sched_urls):
    i =  0
    timer = py_timer()
    for list_var in sched_urls:
        url = list_var[1]
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find('table', class_='basketball compact dms_colors').find('tbody')
        m_url_sco = list(filter(lambda x: x is not None,map(m_url_sco_map, table)))
        for one in m_url_sco:
            url = one[0]
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            match_score = get_match_score(soup, one[1])
            table = soup.find('table', class_='tablesaw compact')
            if table is None:
                continue
            if 'preview' in url:
                print('preview')
                continue
            boxscore = soup.find('div', class_="boxscore-gamedetails")
            teams = list(map(lambda one: one.text, boxscore.findAll('a', style="text-decoration: none;") ))
            allpd_home = []
# 
            rows = table.find_all('tr')
            for tr in rows:
                cols = tr.find_all('td')
                allpd_home.extend(list(map(lambda td: td.text.strip(), cols )))
            
            allpd_away = []

            table = table.findNext('table')
            rows = table.find_all('tr')
            
            if table is None:
                continue

            for tr in rows:
                cols = tr.find_all('td')
                allpd_away.extend(list(map(lambda td: td.text.strip(), cols )))
            # print(allpd_home)

            home_players_data = allpd_parser(allpd_home)
            away_players_data = allpd_parser(allpd_away)
            now = str(int(timer.get_time()))
            home_team_name = match_score[0][0] + '-' + now
            away_team_name = match_score[1][0] + '-' + now

            # sqlo.write_player(home_players_data)

            home_player_names = list(map(lambda player: player[0], home_players_data))
            sqlo.write_team_inst(home_team_name,home_player_names)

            away_player_names = list(map(lambda player: player[0], away_players_data))
            sqlo.write_team_inst(away_team_name,away_player_names)
            home_score = int(match_score[0][1])
            away_score = int(match_score[1][1])

            sqlo.write_match_inst([home_team_name, away_team_name], [home_score, away_score])
            i=i+1

    timer.print_time_elapsed()
    print(str(i))
    print('closing connection to db')

