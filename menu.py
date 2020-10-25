import string
from objects import *
import objects


# Display a list of all characters saved in database
def show_character_list():
    charList = get_character_list()
    skip_line(1)
    if charList:
        for char in charList:
            print(indent(2) + 'Name: ' + str(char[0]) + ', ID: ' + str(char[1]) + "\n")
    else:
        new = input("No saves available, type " + BUTTON + " for new game. Type anything else to return to main menu: ")
        if new.lower() == BUTTON:
            new_game()
            return
        render_menu()
    skip_line(1)


# Begin customization process
def customize_character(Player, pt):
    Player.show_stats()
    skip_line(1)
    print("You have " + str(pt) + " starting points, spend them wisely. \n")
    weapon = input("You have been provided with a lasgun. Enter " + BUTTON +
                   " to view your weapon. Enter any other button to skip: ")
    skip_line(3)
    if weapon.lower() == BUTTON:
        Player.show_inventory()
    skip_line(1)
    print("No additional weapon is available at level 1, you may purchase more upon ascension. \n")
    dist = input("Enter " + BUTTON + " to distribute points. Enter any other button to skip and save for later: ")
    skip_line(3)
    if dist.lower() == BUTTON:
        print("You may input 0 if you don't wish to add points. Warning: undoing choices is not possible. You have " +
              str(pt) + " points.\n")
        Player.customize()
    Player.show_stats()
    return Player


def view_weapons():
    print("Hello world")


def load_player_options(Player):
    userOption = input("Choose your options, type your choice as spelled: ")
    if userOption.lower() == "resume game":
        return
    elif userOption.lower() == "view weapons":
        view_weapons()
        load_player_options(Player)
    elif userOption.lower() == "edit character":
        Player.customize()
        load_player_options(Player)
    else:
        load_player_options(Player)


# Load new game screen
def new_game():
    skip_line(5)
    charID = get_id(0)
    name = input("Enter a name. Inputs with no letter will return to menu: ")
    count = 0
    for letter in list(string.ascii_lowercase):
        if letter not in name.lower():
            count += 1
    if count >= 26:
        render_menu()
        return
    Player = Character(charID, name, 1, BASE_STATS[1][0], BASE_STATS[1][1], BASE_STATS[1][2], BASE_STATS[1][3],
                       BASE_STATS[1][4], BASE_STATS[1][5], BASE_STATS[1][6], BASE_STATS[1][7], START_PTS, 0, 0, 0)
    weaponQuality = get_weapon_quality(LASGUN_ID)
    weaponType = get_weapon_data(LASGUN_ID)[TYPE_NAME]
    Player.fill_inventory(get_id(1), LASGUN_ID, weaponType, weaponQuality)
    return customize_character(Player, START_PTS)


# Allow loading game and change the current characterID
def load_game():
    show_character_list()
    try:
        charID = int(input("Please type in your character id. If you wish to return to menu, enter any letter: \n"))
        cData = get_character_data(charID)
        Player = Character(cData[0], cData[1], cData[2], cData[3], cData[4], cData[5], cData[6], cData[7], cData[8],
                           cData[9], cData[10], cData[11], cData[12], cData[13], cData[14])
        weaponData = get_my_weapons(Player.charID)
        Player.fill_inventory(weaponData[0], weaponData[1], weaponData[2], weaponData[3])
        Player.show_stats()
        return Player
    except ValueError:
        render_menu()


# Delete a character from database and the weapons he owns
def delete_saves():
    show_character_list()
    while True:
        try:
            deleteChar = int(input("Please type the id of the character you wish to kill. If you wish to return to " +
                                   "the menu, enter any letter: \n"))
            delete_character(deleteChar)
        except ValueError:
            render_menu()


# Save current character and weapons to database
def save_game(Player):
    error = True
    while error:
        insurance = input("Are you sure you want to save the game? Enter " + BUTTON + " to confirm: ")
        if insurance.lower() == BUTTON:
            Player.save_character()
            print("The game had been saved")
            render_options(Player)
        else:
            error = False
            render_options(Player)


# Close console and exit the game
def exit_game():
    sys.exit(0)


# Show player stats and give option to edit it
def view_character(Player):
    Player.show_stats()
    print(indent(2) + "Resume Game \n")
    print(indent(2) + "View Weapons \n")
    print(indent(2) + "Edit Character \n")
    load_player_options(Player)


# Load all the options a player can have in the menu
def load_menu():
    userOption = input("Choose your options, type your choice as spelled: ")
    if userOption.lower() == "new game":
        return new_game()
    elif userOption.lower() == "load game":
        return load_game()
    elif userOption.lower() == "delete saves":
        delete_saves()
    elif userOption.lower() == "exit game":
        exit_game()
    else:
        load_menu()


# Load the options, you can save, resume, exit, and customize your character
def load_options(Player):
    userOption = input("Choose your options, type the option as spelled: ")
    if userOption.lower() == "resume game":
        return
    elif userOption.lower() == "view characters":
        view_character(Player)
    elif userOption.lower() == "save game":
        save_game(Player)
    elif userOption.lower() == "exit game":
        exit_game()
    else:
        load_options(Player)


# Create menu and starting screen
def render_menu():
    skip_line(40)
    delay_print("Welcome to Warhammer 40k. The grim dark future of humanity is at hand. \n"
                "Survival is your objective in this bloody galaxy. Please type the following option as given: ")
    skip_line(2)
    print(indent(2) + "New Game \n")
    print(indent(2) + "Load Game \n")
    print(indent(2) + "Delete Saves \n")
    print(indent(2) + "Exit Game \n")
    skip_line(2)
    return load_menu()


# Display the options menu screen
def render_options(Player):
    skip_line(4)
    print("Option Menu \n")
    print(indent(2) + "Resume Game \n")
    print(indent(2) + "View Characters \n")
    print(indent(2) + "Save Game \n")
    print(indent(2) + "Exit Game \n")
    load_options(Player)
