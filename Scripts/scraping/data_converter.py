import more_itertools
import data_converter
import json
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
def minutespergame_conv(string_time):
    return int(string_time.split(':')[0])*60+int(string_time.split(':')[0])
def free_missed_conv(string_ftmissed):
    accomplished=int(string_ftmissed.split('-')[0])
    aggregate=int(string_ftmissed.split('-')[1])
    return (accomplished, aggregate)
def percent_conv(percentage):
    return float(percentage.replace('%', ''))/100
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
def allpd_parser(allpd):
    l = more_itertools.chunked(allpd, 18)
    l2 = list(filter(lambda x: x is not None,map(l2_map , l ) ) ) 
    p_data = list(map(l3_map, l2))
    return p_data
def parse_string(string):
    parse = json.load(string)
    return parse