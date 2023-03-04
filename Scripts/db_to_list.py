import scraping.sqlite_init as db
import os, re, json

# db.create_match_inst_db()

def player_data_map(p_name):
    con,cur = db.init_player_db()

    sqlstring = """
        SELECT isstarter INTEGER,
                position INTEGER,
                minutespergame INTEGER,
                fic REAL,
                offreb INTEGER,
                defreg INTEGER,
                totalreb INTEGER,
                assists INTEGER,
                fouls INTEGER,
                steals INTEGER,
                turnovers INTEGER,
                block INTEGER,
                points INTEGER,
                fgacc INTEGER,
                fgagr INTEGER,
                thrpacc INTEGER,
                thrpagr INTEGER,
                ftacc INTEGER,
                ftagr INTEGER
        FROM players
        WHERE name="{}"
    """.format(p_name)

    cur.execute(sqlstring)
    p = cur.fetchone()
    con.commit()
    con.close()
    # print(p,p_name)
    if p is None:
        # print(p_name,',')
        return False
    return p

def player_data_map1(p):
    if p is None:
        return False
    return player_data_map(p)

def str_parser(str_list):
    hpnl1 = list(filter(lambda c: 0 if c=='[' or c=="'" or c==']' else 1,list(str_list)))
    hpnl = re.sub(pattern=',\s', string=(''.join(hpnl1)), repl=',').split(',')
    # print(hpnl)
    player_data = list(map(player_data_map1, hpnl))
    return player_data

def instance_to_data(match_list):
    team1 = match_list[0]
    team2 = match_list[1]
    
    con, cur = db.init_team_inst_db()
    
    sql_string = """SELECT player_list_ID FROM team_instances WHERE name="{}" """.format(team1)
    cur.execute(sql_string)
    
    # print("fetching: {} {}".format(team1,str_parser(cur.fetchone()[0])))
    hplayer_data = list(map(lambda p: False if p is False else list(p) ,str_parser(cur.fetchone()[0])))
    con.commit()

    sql_string = """SELECT player_list_ID FROM team_instances WHERE name="{}" """.format(team2)
    cur.execute(sql_string)


    aplayer_data = list(map(lambda p: False if p is False else list(p) ,str_parser(cur.fetchone()[0])))

    home_won = 1 if match_list[2] > match_list[3] else 0
    

    con.commit()
    con.close()

    return [[hplayer_data, aplayer_data],home_won]


def init_purified_matches():
    con, cur = db.init_match_inst_db()
    cur.execute("SELECT team_inst1_ID, team_inst2_ID, Score1, Score2 FROM match_instances")
    l= list(map(lambda match: instance_to_data(match), cur.fetchall()))
    # X[<r>] = team 
    l_filter = []
    p= len(l)
    

    for i in range(p):
        X_match = l[i][0]
        team1 = X_match[0]
        team2 = X_match[1]
        # print(False in X_team)
        if  (not (False in team1)) and (not (False in team2)) :
            print('plz')
            l_filter.append(l[i])

    path = os.getcwd()
    print(l_filter)
    with open('{}/Scripts/ai/list_data.json'.format(path), 'w') as f:
        json.dump((l_filter), f)
init_purified_matches()