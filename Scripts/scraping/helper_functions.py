import bs4.element
import requests
from bs4 import BeautifulSoup
import sqlite_operations as sqlo
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
def get_match_date(soup):
    date_str = soup.find('strong').text.strip()
    #date = datetime.datetime.strptime(date_str, '%B %d, %Y')
    return date_str
def get_player_url(table):
    rows = table.findAll('tr')
    p_url = rows.find('td')['href']
    return p_url
def hydrate_allpd(rows):
    allpd = []
    for tr in rows:
        cols = tr.find_all('td')
        allpd.extend(list(map(lambda td: td.text.strip(), cols )))
    return allpd
def write_full_match(allpd_home, allpd_away, match_score, match_date):
    home_players_data = allpd_parser(allpd_home)
    away_players_data = allpd_parser(allpd_away)
    home_team_name = match_score[0][0] + '-'  + match_date
    away_team_name = match_score[1][0] + '-' +  match_date

    # sqlo.write_player(home_players_data)

    home_player_names = list(map(lambda player: player[0], home_players_data))
    sqlo.write_team_inst(home_team_name,home_player_names)

    away_player_names = list(map(lambda player: player[0], away_players_data))
    sqlo.write_team_inst(away_team_name,away_player_names)
    home_score = int(match_score[0][1])
    away_score = int(match_score[1][1])

    sqlo.write_match_inst([home_team_name, away_team_name], [home_score, away_score])
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
