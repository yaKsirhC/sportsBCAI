import sqlite3


def init_player_db():
    con = sqlite3.connect('1.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS players (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name text,
                isstarter text,
                position text,
                minutespergame text,
                fgmissed text,
                threepointsmiss text,
                ftmissed text,
                fic integer,
                offreb integer,
                defreg integer,
                totalreb integer,
                assists integer,
                fouls integer,
                steals integer,
                turnovers integer,
                block integer,
                points integer)""")

    return (con,cur)