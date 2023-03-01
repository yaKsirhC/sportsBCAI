from sqlite_init import init_player_db

con, cur = init_player_db()

print(cur.fetchone())

"""
    [17,17,2]
"""