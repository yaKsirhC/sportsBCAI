import os

size1 = os.path.getsize('/home/chris-kay/Documents/py/sportsBCAI/players.db')
size2 = os.path.getsize('/home/chris-kay/Documents/py/sportsBCAI/team_instances.db')
size3 = os.path.getsize('/home/chris-kay/Documents/py/sportsBCAI/match_instances.db')

print(f"{(size1+size2+size3)/1000}kb") 