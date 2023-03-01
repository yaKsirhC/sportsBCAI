def minutespergame_conv(string_time):
    return int(string_time.split(':')[0])*60+int(string_time.split(':')[0])
def free_missed_conv(string_ftmissed):
    accomplished=int(string_ftmissed.split('-')[0])
    aggregate=int(string_ftmissed.split('-')[1])
    return (accomplished, aggregate)
def percent_conv(percentage):
    return float(percentage.replace('%', ''))/100