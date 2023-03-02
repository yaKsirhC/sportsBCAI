import bs4.element
import requests
from bs4 import BeautifulSoup
from sqlite_init import init_player_db
import get_sched_urls
import more_itertools
import data_converter


con, cur = init_player_db()

player_position_dict = {'': 0,'SG': 1, 'C': 2, 'SF': 3, 'PG': 4, 'PF': 5}
starter_dict = {'Starter': 0, 'Bench': 1}


print('scraping data')
sched_urls = get_sched_urls.get_sched_urls()
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

        # print(allpd_home)
        if len(allpd_home) < 17:
            print(f'lenght of statistics: {len(allpd_home)}')
            print('No data for current player')
            continue
        else:
            l = more_itertools.chunked(allpd_home, 18)
            l2 = []
            for a in l:
                a.pop(0)
                if a[0] == 'Team':
                    continue
                elif a[0] == '':
                    continue
                else:
                    l2.append(a)
        # print(l2)
        l3 = []
        for l in l2:
            print(l)
            l[1] = starter_dict[l[1]]

            l[2] = player_position_dict[l[2]]
            l[3] = data_converter.minutespergame_conv(l[3])
            fmacc, fmagr = (data_converter.free_missed_conv(l[4]))
            thrpacc, thrpagr = (data_converter.free_missed_conv(l[5]))
            ftacc, ftagr = (data_converter.free_missed_conv(l[6]))
            shots_list = [fmacc, fmagr, thrpacc, thrpagr, ftacc, ftagr]
            l.extend(shots_list)
            l[7] = float(l[7])
            l[8:17] = [eval(i) for i in l[8:17]]
            del l[4:7]
            l3.append(l)

        print('Writing to DB')

        for i in range(len(l3)):
            isIn = cur.execute("SELECT ? FROM players", l3[i][0])
            if isIn:
                print(f'player {l3[i][0]}')
                continue
            sql_str = """INSERT INTO players VALUES (NULL,"{}", "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(l3[i][0], l3[i][1], l3[i][2], l3[i][3], l3[i][4], l3[i][5], l3[i][6], l3[i][7],l3[i][8], l3[i][9], l3[i][10], l3[i][11], l3[i][12],
l3[i][13], l3[i][14], l3[i][15], l3[i][16], l3[i][17]
, l3[i][18], l3[i][19])
            # print(sql_str)
            cur.execute(sql_str)
            # print(f"Fetching all: {cur.fetchall()}")

print('closing connection to db')
con.commit()
con.close()
