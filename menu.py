from objects import *
import string


def show_character_list():
    charList = get_character_list()
    skip_line(1)
    if charList:
        for char in charList:
            print(indent(2) + 'Name: ' + str(char[0]) + ', ID: ' + str(char[1]) + "\n")
    else:
        new = input("No saves available, type start for new game. Type anything else to return to main menu: ")
        if new.lower() == "start":
            new_game()
            return
        render_menu()
    skip_line(1)


def show_weapon_data(weapon):
    wData = get_weapon_data(weapon)
    for attr in wData:
        print(attr)


def show_character(charID):
    cData = get_character_data(charID)
    for i, attr in enumerate(BASE_STATS[0]):
        print(attr + ": " + str(cData[i]))


def add_weapons(wID, quality, typeID):
    Weapon1 = Weapon(wID, quality, typeID)
    return


def customize_character(pt):
    skip_line(1)
    Player.show_stats()
    skip_line(1)
    print("You have " + str(pt) + " starting points, spend them wisely. \n")
    weapon = input("You have been provided with a lasgun. Enter w to view your weapon. Any other button to skip: ")
    skip_line(3)
    if weapon.lower() == "w":
        show_weapon_data("Lasgun")
    print("No additional weapon is available at level 1, you may purchase more upon ascension. \n")
    dist = input("Enter d to distribute points. Enter any other button to skip and save for later: ")
    skip_line(3)
    print("You may input 0 if you don't wish to add points. Warning: undoing choices is not possible. You have " +
          str(pt) + " points.\n")
    if dist.lower() == "d":
        Player.customize()
    skip_line(1)
    Player.show_stats()


# Load new game screen
def new_game():
    skip_line(5)
    global Player
    charID = get_id(0)
    if charID == 0:
        print("You have too many saves. You must delete some.")
        delete_saves()
    name = input("Enter a name. Inputs with no letter will return to menu: ")
    count = 0
    for letter in list(string.ascii_lowercase):
        if letter not in name.lower():
            count += 1
    if count >= 26:
        render_menu()
        return
    Player = Characters(charID, name, 1, BASE_STATS[1][0], BASE_STATS[1][1], BASE_STATS[1][2], BASE_STATS[1][3],
                        BASE_STATS[1][4], BASE_STATS[1][5], START_PTS)
    Player.fill_inventory(1, 1)
    add_weapons(get_id(1), get_weapon_quality(1), 1)
    customize_character(START_PTS)


# Allow loading game and change the current characterID
def load_game():
    global currScene
    global Player
    show_character_list()
    try:
        charID = int(input("Please type in your character id. If you wish to return to menu, enter any letter: \n"))
        currScene = get_curr_progress(charID)
        cData = get_character_data(charID)
        Player = Characters(cData[0], cData[1], cData[2], cData[3], cData[4], cData[5], cData[6], cData[7], cData[8],
                            cData[9])
        return
    except ValueError:
        render_menu()


def delete_saves():
    show_character_list()
    while True:
        try:
            deleteChar = int(input("Please type the id of the character you wish to kill. If you wish to return to " +
                                   "the menu, enter any letter: \n"))
            delete_character(deleteChar)
        except ValueError:
            render_menu()


def save_game():
    error = True
    while error:
        insurance = input("Are you sure you want to save the game (Y/N)?")
        if insurance.lower() == "y":
            if not_in_database(Player.charID):
                insert_character(Player.charID, Player.name, Player.level, Player.data, Player.freePoints)
            else:
                update_character(Player.charID, Player.level, Player.data, Player.freePoints)

            return
        elif insurance.lower() == "n":
            error = False
            render_options()


def exit_game():
    sys.exit(0)


# Load all the options a player can have in the menu
def load_menu():
    userOption = input("Choose your options: ")
    if userOption.lower() == "new game":
        new_game()
    elif userOption.lower() == "load game":
        load_game()
    elif userOption.lower() == "delete saves":
        delete_saves()
    elif userOption.lower() == "exit game":
        exit_game()
    else:
        load_menu()


def load_options():
    userOption = input("Choose your options: ")
    if userOption.lower() == "resume game":
        return
    elif userOption.lower() == "save game":
        save_game()
    elif userOption.lower() == "exit game":
        exit_game()
    else:
        load_menu()


# Create menu and starting screen
def render_menu():
    skip_line(40)
    delay_print("Welcome to Warhammer 40k. The grim dark future of humanity is at hand. \n"
                "Survival is your objective in this bloody galaxy. Please type the following option as given\n")
    print(indent(2) + "New Game \n")
    print(indent(2) + "Load Game \n")
    print(indent(2) + "Delete Saves \n")
    print(indent(2) + "Exit Game \n")
    load_menu()
    skip_line(10)


def render_options():
    skip_line(4)
    print("Option Menu \n")
    print(indent(2) + "Resume Game \n")
    print(indent(2) + "Save Game \n")
    print(indent(2) + "Exit Game \n")
    load_options()
    skip_line(10)
