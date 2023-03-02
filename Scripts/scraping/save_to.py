def save_to_db(allpd):
    # print(allpd_home)
    if len(allpd_home) < 17:
        print(f'lenght of statistics: {len(allpd_home)}')
        print('No data for current player')
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
        sql_str = """INSERT INTO players VALUES (NULL,"{}", "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(
            l3[i][0], l3[i][1], l3[i][2], l3[i][3], l3[i][4], l3[i][5], l3[i][6], l3[i][7], l3[i][8], l3[i][9],
            l3[i][10], l3[i][11], l3[i][12],
            l3[i][13], l3[i][14], l3[i][15], l3[i][16], l3[i][17]
            , l3[i][18], l3[i][19])
        # print(sql_str)
        cur.execute(sql_str)
        # cur.execute("SELECT * FROM players")
        # print(f"Fetching all: {cur.fetchall()}")
