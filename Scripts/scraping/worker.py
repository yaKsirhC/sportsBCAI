import bs4.element
import requests
from bs4 import BeautifulSoup
from sqlite_operations import save_to_db
from timer import py_timer


def m_url_sco_map(row):
    if isinstance(row, bs4.element.Tag):
        d = row.find('td').findNextSibling('td').findNextSibling('td').find('a')
        if d is None:
            return
        match_url = "https://basketball.realgm.com/" + d['href']
        match_score = d.text
        return [match_url, match_score]

def worker(sched_urls):
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
            table = soup.find('table', class_='tablesaw compact')
            if table is None:
                continue
            if 'preview' in url:
                print('preview')
                continue
            boxscore = soup.find('div', class_="boxscore-gamedetails")
            teams = list(map(lambda one: one.text, boxscore.findAll('a', style="text-decoration: none;") ))
            allpd_home = []

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
                allpd_away = list(map(lambda td: td.text.strip(), cols ))
            # print(allpd_home)
            save_to_db(allpd_home)

    timer.print_time_elapsed()
    print('closing connection to db')
