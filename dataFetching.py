import sqlite3 as sq

# identify location of database, courtesy of Monika Richardson
con = sq.connect("database/vilinius.db")
c = con.cursor()

#
currScene = 1
currChar = 0
TIME_STOP = 0

intro = open('database/intro.txt', 'r')
introContent = intro.read()


def get_character():
    sql = c.execute('SELECT * FROM Characters')
    data = c.fetchall()
    print(data)


def insert_character(charName):
    insertion = ('INSERT INTO Characters(CharName, CharLevel, Strength, '
                 'Endurance, Durability, Agility, Accuracy, InventoryCap) Values ("' + str(charName) + '", 1, 10, 10, 10, 10, 10, 10)')
    sql = c.execute(insertion)
    con.commit()


def delete_character(charID):
    insertion = ('DELETE FROM Characters WHERE CharID = ' + str(charID))
    sql = c.execute(insertion)
    con.commit()


def get_id():
    sql = c.execute('SELECT Count() FROM Characters')
    data = c.fetchall()
    return data


def get_character_list():
    sql = c.execute("SELECT CharName, CharID FROM Characters")
    data = c.fetchall()
    return data


