from colorama import Fore
from sqlite_init import init_team_inst_db, init_match_inst_db, init_player_db
import re



def write_player(p_data):
    con, cur = init_player_db()
    for i in range(len(p_data)):
        if p_data[i][0].find("'"):
            p_data[i][0] = re.sub(string=p_data[i][0], pattern="'", repl=" ")
        cur.execute('SELECT * FROM players WHERE name="{}"'.format(p_data[i][0]))
        fetch = cur.fetchone()
        if fetch:
            print('Player '+ Fore.YELLOW + str(p_data[i][0]) + Fore.WHITE + ' exists in db.')
            continue

        print('Writing player '+ Fore.CYAN + str(p_data[i][0]) + Fore.WHITE + ' in database.')
        with open('file.txt', 'a+') as f:
            f.write("\n{}".format(p_data[i][0]))
        sql_str = """INSERT INTO players VALUES (NULL,"{}", "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(
            p_data[i][0], p_data[i][1], p_data[i][2], p_data[i][3], p_data[i][4], p_data[i][5], p_data[i][6], p_data[i][7], p_data[i][8], p_data[i][9],
            p_data[i][10], p_data[i][11], p_data[i][12],
            p_data[i][13], p_data[i][14], p_data[i][15], p_data[i][16], p_data[i][17]
            , p_data[i][18], p_data[i][19])
        cur.execute(sql_str)
        con.commit()
    con.close()

def write_team_inst(name, p_list):
    con, cur = init_team_inst_db()
    sql_str_find = """SELECT * FROM team_instances WHERE name={}""".format(name)

    cur.execute(sql_str_find)
    if cur.fetchone():
        print('{} team instance already exists in db.'.format(name))
        return

    parsed_p_list = list(map(lambda string_name: re.sub(string=string_name,pattern="'", repl=" "), p_list ))
    sql_str = """INSERT INTO team_instances VALUES (NULL, "{}", "{}")""".format(name, parsed_p_list)

    print('Writing team '+ Fore.GREEN + str(name) + Fore.WHITE + ' in database.')
    cur.execute(sql_str)
    con.commit()
    con.close()

def write_match_inst(team_list, score_list ):
    con, cur = init_match_inst_db()
    team1, team2 = team_list
    score1, score2 = score_list
    sql_str = """INSERT INTO match_instances VALUES (NULL,"{}", "{}", {}, {})""".format(team1, team2, score1, score2)
    # print(sql_str)
    print('Writing match '+ Fore.BLUE + str(team1) + "vs"+ str(team2) + Fore.WHITE + ' in database.')
    cur.execute(sql_str)
    con.commit()
    con.close()