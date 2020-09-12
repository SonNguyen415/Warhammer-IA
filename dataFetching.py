import sqlite3 as sq

# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()


def insert_character(characterName, Rank, charID):
    insertion = ('INSERT INTO Characters(CharacterName, CharacterLevel, CharacterID) Values ("' + str(characterName) + '", "' + str(Rank) + '", "' + str(charID) + ')');
    sql = c.execute(insertion)


def get_id():
    sql = c.execute('SELECT CharacterID FROM Characters WHERE CharacterID = Count()')
    data = c.fetchall()
    return data


def get_character_list():
    sql = c.execute("SELECT CharacterName, CharacterID FROM Characters")
    data = c.fetchall()
    return data

