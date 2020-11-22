import string
from objects import *


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
            return new_game()
        return render_menu()
    skip_line(1)


# Initial customization process, player can distribute their current free points towards their character
def customize_character(Player):
    Player.show_stats()
    skip_line(1)
    print("You have " + str(START_PTS) + " starting points, spend them wisely. \n")
    weapon = input("You have been provided with a lasgun. Enter " + BUTTON +
                   " to view your weapon. Enter any other button to skip: ")
    skip_line(3)
    if weapon.lower() == BUTTON:
        Player.show_inventory()
    skip_line(2)
    print("No additional weapon is available at level 1, you may purchase more upon ascension. \n")
    dist = input("Enter " + BUTTON + " to distribute points. Enter any other button to skip and save for later: ")
    skip_line(3)
    if dist.lower() == BUTTON:
        print("You may input 0 if you don't wish to add points. Warning: undoing choices is not possible. You have " +
              str(START_PTS) + " points.\n")
        Player.customize()
    Player.show_stats()
    return Player


# Display all weapons in inventory and ask if player wants to discard any
def view_weapons(Player):
    Player.show_inventory()
    try:
        selection = int(input("Select a weapon id to discard from your inventory. "
                              "Enter any letter if you don't want to discard any: "))
        Player.remove_inventory(selection)
        return Player
    except ValueError:
        return Player


# Get weapon list that player can purchase and inquire upon their purchase. Tell them if they can't buy a weapon and why
def purchase_weapons(Player):
    weaponList = get_purchasable_weapons(Player.level)
    print("You have " + str(Player.freeInventory) + " units of free space in your inventory \n")
    print("You have  " + str(Player.freePoints) + " free points you can spend. \n")
    for weapon in weaponList:
        print(("TypeID: " + str(weapon[0]), "Weapon Type: " + str(weapon[1]), "Weapon Size: " + str(weapon[2]),
               "Weapon Cost: " + str(weapon[3])))
    skip_line(2)
    try:
        buyWeapon = int(input("Select the id of the weapon you want to buy. Enter any letter if you won't buy "
                              "anything: "))
        weaponData = get_weapon_data(buyWeapon)
        while weaponData[WEAPON_COST] > Player.freePoints:
            buyWeapon = int(input("You don't have enough points to purchase this. Please select another id: "))
            weaponData = get_weapon_data(buyWeapon)
        while weaponData[WEAPON_SIZE] > Player.freeInventory:
            buyWeapon = int(input("You don't have enough space in your inventory for this weapon. Please select "
                                  "another id: "))
            weaponData = get_weapon_data(buyWeapon)
        Player.fill_inventory(get_id(1), weaponData[TYPE_ID], weaponData[TYPE_NAME], weaponData[WEAPON_RELIABILITY])
        return Player
    except ValueError:
        return Player


# Load the view character options
def load_character_options(Player):
    userOption = input("Choose your options, type your choice as spelled: ")
    if userOption.lower() == "resume game":
        return Player
    elif userOption.lower() == "view weapons":
        return view_weapons(Player)
    elif userOption.lower() == "edit character":
        Player.customize()
        skip_line(2)
        return load_character_options(Player)
    elif userOption.lower() == "purchase weapons":
        return purchase_weapons(Player)
    else:
        return load_character_options(Player)


# Show player stats and give option to edit it
def view_character(Player):
    Player.show_stats()
    print(indent(2) + "Resume Game \n")
    print(indent(2) + "View Weapons \n")
    print(indent(2) + "Edit Character \n")
    print(indent(2) + "Purchase Weapons \n")
    return load_character_options(Player)


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
        return render_menu()
    Player = Character(charID, name, 1, BASE_STATS[1][INITIATIVE], BASE_STATS[1][HEALTH], BASE_STATS[1][STRENGTH], 
                       BASE_STATS[1][ENDURANCE], BASE_STATS[1][DURABILITY], BASE_STATS[1][AGILITY], BASE_STATS[1][ACCURACY], 
                       BASE_STATS[1][INVENTORY_CAP], START_PTS, 0, 0, 0, 1)
    weaponData = get_weapon_data(LASGUN_ID)
    Player.fill_inventory(get_id(1), weaponData[TYPE_ID], weaponData[TYPE_NAME], weaponData[WEAPON_RELIABILITY])
    return customize_character(Player)


# Allow loading game and change the current characterID
def load_game():
    show_character_list()
    cData = 0
    while cData == 0:
        try:
<<<<<<< Updated upstream
            charID = int(input("Please type in your character id. If you wish to return to menu, enter any letter: \n"))
=======
            charID = int(
                input("Please type in a valid id. If you wish to return to menu, enter any letter: \n"))
>>>>>>> Stashed changes
            cData = get_character_data(charID)
        except ValueError:
            return render_menu()
    Player = Character(cData[0], cData[1], cData[2], cData[3], cData[4], cData[5], cData[6], cData[7], cData[8],
<<<<<<< Updated upstream
                               cData[9], cData[10], cData[11], cData[12], cData[13], cData[14], cData[15])
=======
                       cData[9], cData[10], cData[11], cData[12], cData[13], cData[14], cData[15])
>>>>>>> Stashed changes
    weaponData = get_my_weapons(Player.charID)
    Player.fill_inventory(weaponData[0], weaponData[1], weaponData[2], weaponData[3])
    Player.show_stats()
    return Player


# Delete a character from database and the weapons he owns
def delete_saves():
    show_character_list()
    deleting = True
    while deleting:
        try:
            deleteChar = int(input("Please type the id of the character you wish to kill. If you wish to return to " +
                                   "the menu, enter any letter: \n"))
            delete_character(deleteChar)
        except ValueError:
            deleting = False
    return render_menu()


# Save current character and weapons to database
def save_game(Player):
    error = True
    while error:
        insurance = input("Are you sure you want to save the game? Enter " + BUTTON + " to confirm: ")
        if insurance.lower() == BUTTON:
            Player.save_character()
            print("The game had been saved")
            return render_options(Player)
        else:
            error = False
            return render_options(Player)


# Close console and exit the game
def exit_game():
    sys.exit(0)


# Load all the options a player can have in the menu
def load_menu():
    userOption = input("Choose your options, type your choice as spelled: ")
    if userOption.lower() == "new game":
        return new_game()
    elif userOption.lower() == "load game":
        return load_game()
    elif userOption.lower() == "delete saves":
        return delete_saves()
    elif userOption.lower() == "exit game":
        exit_game()
    else:
        return load_menu()


# Load the options, you can save, resume, exit, and customize your character
def load_options(Player):
    userOption = input("Choose your options, type the option as spelled: ")
    if userOption.lower() == "resume game":
        return
    elif userOption.lower() == "view characters":
        return view_character(Player)
    elif userOption.lower() == "save game":
        return save_game(Player)
    elif userOption.lower() == "exit game":
        exit_game()
    else:
        return load_options(Player)


# Create menu and starting screen
def render_menu():
    skip_line(40)
    print("Disclaimer: This is a fan work. Warhammer 40k and all its content belongs to Games Worshop")
    skip_line(2)
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
    return load_options(Player)
