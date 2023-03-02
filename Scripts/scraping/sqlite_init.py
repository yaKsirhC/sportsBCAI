import sqlite3


def init_player_db():
    con = sqlite3.connect('1.db', )
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS players (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT,
                isstarter INTEGER,
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
                )""")
    
    #20

    return (con,cur)