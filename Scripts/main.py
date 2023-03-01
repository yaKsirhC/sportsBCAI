import bs4.element
import requests
from bs4 import BeautifulSoup
from sqlite_init import init_player_db
import get_sched_urls

con, cur = init_player_db()

print('scraping data')
sched_urls = get_sched_urls.get_sched_urls()
for list in sched_urls:
    url = list[1]
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    table = soup.find('table', class_='basketball compact dms_colors').find('tbody')

    m_url_sco = []
    for row in table:
        if isinstance(table, bs4.element.Tag):
            d = table.find('td').findNextSibling('td').findNextSibling('td').find('a')
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
        allpd_home = []
        if table is not None:
            rows = table.find_all('tr')
            for tr in rows:
                cols = tr.find_all('td')
                for td in cols:
                    allpd_home.append(td.text.strip())
            table = table.findNext('table')
        allpd_away = []
        if table is not None:
            rows = table.find_all('tr')
            for tr in rows:
                cols = tr.find_all('td')
                for td in cols:
                    allpd_away.append(td.text.strip())

    print(allpd_home)
    if len(allpd_home) < 17:
        print('No data for current player')
        continue
    print('Writing to DB')
    cur.execute("INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                    "?, ?, ?, ?, ?, ?, ?)", (None, allpd_home[0], allpd_home[1], allpd_home[2],
                                          allpd_home[3],
                                          allpd_home[4], allpd_home[5], allpd_home[6],
                                          allpd_home[7],
                                          allpd_home[8], allpd_home[9], allpd_home[10],
                                          allpd_home[11],
                                          allpd_home[12], allpd_home[13], allpd_home[14],
                                          allpd_home[15],
                                          allpd_home[16]))
print(cur.fetchall())
print('closing connection to db')
con.commit()
con.close()