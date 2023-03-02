import bs4.element
import requests
from bs4 import BeautifulSoup
from sqlite_init import init_player_db
from sqlite_operations import save_to_db
import time

start = time.time()
con, cur = init_player_db()

def worker(sched_urls):
    for list in sched_urls:
        url = list[1]
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find('table', class_='basketball compact dms_colors').find('tbody')

        m_url_sco = []
        for row in table:
            if isinstance(row, bs4.element.Tag):
                d = row.find('td').findNextSibling('td').findNextSibling('td').find('a')
                try:
                    match_url = "https://basketball.realgm.com/" + d['href']
                    match_score = d.text
                    m_url_sco.append([match_url, match_score])
                except TypeError:
                    continue

        for one in m_url_sco:
            url = one[0]
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            table = soup.find('table', class_='tablesaw compact')
            if 'preview' in url:
                continue
            boxscore = soup.find('div', class_="boxscore-gamedetails")
            teams = []
            for one in boxscore.findAll('a', style="text-decoration: none;"):
                teams.append(one.text)
            allpd_home = []
            if table is not None:
                rows = table.find_all('tr')
                for tr in rows:
                    cols = tr.find_all('td')
                    for td in cols:
                        allpd_home.append(td.text.strip())
            allpd_away = []
            if table is not None:
                table = table.findNext('table')
                rows = table.find_all('tr')
                for tr in rows:
                    cols = tr.find_all('td')
                    for td in cols:
                        allpd_away.append(td.text.strip())

            save_to_db(allpd_home)
    
    end = time.time()
    dt = (end - start)
    print('Took ' + str(round(dt, 8)) + 's')

    print('closing connection to db')
    con.commit()
    con.close()
    return worker