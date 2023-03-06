import bs4.element
import requests
from bs4 import BeautifulSoup
from timer import py_timer
from data_converter import allpd_parser
from helper_functions import get_match_date, get_match_score, m_url_sco_map, get_player_url, hydrate_allpd, write_full_match
import more_itertools
# import sqlite_operations as sqlo

def get_team_name_f_sched(url):
    team_name = url.split('/')[-2]
    return team_name

def tp_stats(list):
    p_total_stats = []
    for p in list:
        for p3 in p:
            p2 = p3.split('\n')
            print("p is: ")
            p2[3:5] = [int(x) for x in p2[3:5]]
            p2[5:25] = [float(x) for x in p2[6:25]]
            p_total_stats.append(p2)
    return p_total_stats


def proc_total_p_stats(list_var):
    l = more_itertools.chunked(list_var, 24)
    p_total_stats = tp_stats(l)
    return p_total_stats

def get_total_player_stats(url, team):
    req2 = requests.get(url)
    soup = BeautifulSoup(req2.text, 'html.parser')
    t = soup.select_one("[name='International']+h1+p+h2+*") # ksexases to `+table` ? 
    p_name0 = soup.find('h2', style="margin-top: 0;").text
    p_name = p_name0.split('\xa0SF')[0]
    tbody = t.find('tbody')
    rows = tbody.findAll(lambda tag: tag.name=='tr')
    list = [c.text.strip() for c in rows]
    print(p_name) 
    p_stats = proc_total_p_stats(list)
    return p_stats

def get_players_url_f_match(table):
    table = table.tbody.findAll('tr')
    p_urls = []
    for row in table:      
        p_url = row.findAll('td')[1].a['href']
        p_url = str('https://basketball.realgm.com') + str(p_url)
        p_urls.append(p_url)
        print(p_urls)
    return p_urls

def worker(sched_urls):
    i =  0
    timer = py_timer()
    for list_var in sched_urls:
        url = list_var[1]
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find('table', class_='basketball compact dms_colors').find('tbody')
        m_url_sco = list(filter(lambda x: x is not None,map(m_url_sco_map, table))) #
        c = 0
        for one in m_url_sco:
            url = one[0]
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')

            match_score = get_match_score(soup, one[1])
            match_date = get_match_date(soup)
        
            table = soup.find('table', class_='tablesaw compact')
#            if c == 0:
#                t_name = get_team_name_f_sched(list_var[1])
#                p_url_list = get_players_url_f_match(table)
#                home_p_stats = []
#                for pl_url in p_url_list:
#                    print('player')
#                    home_p_stats.append(get_total_player_stats(pl_url, t_name))
#                    print(home_p_stats)
#            c += 1
#
            if table is None or 'preview' in url:
                continue
            rows = table.find_all('tr')
            allpd_home = hydrate_allpd(rows)

            table = table.findNext('table') 

            if table is None:
                continue
            rows = table.find_all('tr')
            allpd_away = hydrate_allpd(rows)
            write_full_match(allpd_home, allpd_away, match_score, match_date)
            i=i+1
            c=c+1

    timer.print_time_elapsed()
    print(str(i))
    print('closing connection to db')

