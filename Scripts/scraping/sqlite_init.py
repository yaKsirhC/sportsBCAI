import sqlite3

def init_player_db():
    con = sqlite3.connect('players.db', )
    cur = con.cursor()
    return (con,cur)
def create_player_db():
    con = sqlite3.connect('players.db', )
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
def init_team_inst_db():
    con = sqlite3.connect('team_instances.db')
    cur = con.cursor()
    return (con,cur)
def create_team_inst_db():
    con = sqlite3.connect('team_instances.db')
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team_instances(
            TeamID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT,
            player_list_ID TEXT
        )
    """)
def init_match_inst_db():
    con = sqlite3.connect('match_instances.db')
    cur = con.cursor()
    return (con,cur)
def create_match_inst_db():
    con = sqlite3.connect('match_instances.db')
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS match_instances(
            MatchID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            team_inst1_ID TEXT,
            team_inst2_ID TEXT,
            Score1 INTEGER,
            Score2 INTEGER,
            FOREIGN KEY(team_inst1_ID) REFERENCES team_instances(name),
            FOREIGN KEY(team_inst2_ID) REFERENCES team_instances(name)
        )
    """)