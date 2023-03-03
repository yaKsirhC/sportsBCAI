import more_itertools
from sqlite_init import init_player_db
import data_converter
from colorama import Fore

player_position_dict = {'': 0, 'SG': 1, 'C': 2, 'SF': 3, 'PG': 4, 'PF': 5}
starter_dict = {'Starter': 0, 'Bench': 1}

def l3_map(l):
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
    return l
def l2_map(a):
    a.pop(0)
    if not (a[0] == 'Team' or a[0] == ''):
        return a

def save_to_db(allpd):
    con, cur = init_player_db()
    l = more_itertools.chunked(allpd, 18)
    l2 = list(filter(lambda x: x is not None,map(l2_map , l ) ) )   
    l3 = list(map(l3_map, l2))

    for i in range(len(l3)):
        cur.execute('SELECT * FROM players WHERE name="{}"'.format(l3[i][0]))
        fetch = cur.fetchone()
        if fetch:
            print('Player '+ Fore.YELLOW + str(l3[i][0]) + Fore.WHITE + ' exists in db.')
            continue
        print('Writing player '+ Fore.CYAN + str(l3[i][0]) + Fore.WHITE + ' in database.')
        sql_str = """INSERT INTO players VALUES (NULL,"{}", "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(
            l3[i][0], l3[i][1], l3[i][2], l3[i][3], l3[i][4], l3[i][5], l3[i][6], l3[i][7], l3[i][8], l3[i][9],
            l3[i][10], l3[i][11], l3[i][12],
            l3[i][13], l3[i][14], l3[i][15], l3[i][16], l3[i][17]
            , l3[i][18], l3[i][19])
        # print(sql_str)
        cur.execute(sql_str)
        con.commit()
    con.close()
