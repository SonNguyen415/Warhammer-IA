import sqlite3 as sq

# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()

#
currScene = 1
currCHAR = 0
TIME_STOP = 0


def insert_character(charName):
    insertion = ('INSERT INTO Characters(CharName, CharLevel, Strength, '
                 'Endurance, Durability, Agility, Accuracy, InventoryCap) Values ("' + str(charName) + '", 1, 10, 10, 10, 10, 10, 10)')
    sql = c.execute(insertion)


def get_id():
    sql = c.execute('SELECT Count() FROM Characters')
    data = c.fetchall()
    return data


def get_character_list():
    sql = c.execute("SELECT CharName, CharID FROM Characters")
    data = c.fetchall()
    return data

