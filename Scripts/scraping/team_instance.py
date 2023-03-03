import more_itertools
import requests
from bs4 import BeautifulSoup
import bs4.element
import sqlite_init
from timer import py_timer

timer = py_timer()

con, cur = sqlite_init.init_player_db()
url = 'https://basketball.realgm.com/international/league/1/Euroleague/team/142/ALBA-Berlin/schedule' # einai constant den alazei
req = requests.get(url)
teams_dict = {1: 'ALBA-Berlin', 2: 'Anadolu-Efes', 3: 'AS-Monaco-Basket',
 4: 'ASVEL-Basket', 5: 'AX-Armani-Exchange-Milan', 6: 'Barca', 7: 'Baskonia',
 8: 'Bayern-Munich', 9: 'Fenerbahce-Beko', 10: 'KK-Crvena-Zvezda', 11: 'KK-Partizan',
 12: 'Maccabi-FOX-Tel-Aviv', 13: 'Olympiacos', 14: 'Panathinaikos', 15: 'Real-Madrid',
 16: 'Valencia-Basket', 17: 'Virtus-Bologna', 18: 'Zalgiris'}

def get_all_teams_map(team):
    if isinstance(team, bs4.element.Tag):
            team_name = str(team['href']).split('/')[-1]
            team_players_url = "https://basketball.realgm.com/" + team['href'] + '/players'
            return [team_name, team_players_url]



def get_player_id(p_name):
    cur.execute('SELECT * FROM players WHERE name="{}"'.format(p_name))
    isin = cur.fetchone()
    if isin:
        p_id = isin[0]
        return p_id
    return 0

def get_year_schedule():
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    year_sched = soup.find('div', class_='page-nav-option clearfix')
    l = year_sched.findAll('option')
    year_sched = list(map(lambda a: a['value'], l))
    # print(year_sched)

get_year_schedule()


def get_team_urls():
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    teams = soup.find('div', id='teamnav').findAll('a', href=True)
    allteams = list(filter(lambda x: x is not None, map(get_all_teams_map, teams)))
    # print(allteams)
    return allteams

def t2_map(a):
    if not ((a=='Team') and (a=='')):
        return a

sched_urls = get_team_urls()
for list_var in sched_urls:
    url = list_var[1]
    team = list_var[0] # that's the team name? nai
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    team_players = []
    for tr in rows:
        player = tr.find_all('td')
        team_players = list(map(lambda data: data.text.strip(), player))
    t1 = more_itertools.chunked(team_players, 8)
    t2 = list(filter(lambda a: a is not None ,map(t2_map, t1)))
    p_ids = []
    for player in t2:
        p_id = get_player_id(player[0])
        print("player id is: " + str(p_id))
        if p_id == 0:
            print("player not in list " + str(player[0]))
            continue
        p_ids.append(p_id)
        print("player id is: " + str(p_id))
    sqlite_init.init_team_inst_db()
    # cur.execute("INSERT INTO team_instance (TeamID, name, Player_IDS) VALUES (NULL, {} , {} )".format(team_name,player_id_list)),
    # (team, p_ids) ???? to onoma tis omadas kai player ids
    # ego to evala, tha ta simblirosoume meta
    con.commit()
    
print("complete")
con.close()
timer.print_time_elapsed()
