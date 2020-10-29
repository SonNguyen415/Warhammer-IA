from data import *
import math


class Weapon(object):
    def __init__(self, wID, typeID, weaponType, weaponQuality):
        self.wID = wID
        self.typeID = typeID
        self.maxQuality = weaponQuality
        self.quality = self.maxQuality
        self.size = get_weapon_data(typeID)[WEAPON_SIZE]
        self.weaponType = weaponType

    # Damage the weapons due to use
    def lower_quality(self):
        self.quality -= 2
        if self.quality <= 0:
            print("This weapon is now broken.")
            self.quality = 0

    # Show weapon data
    def display_weapon(self):
        print(("Weapon ID: " + str(self.wID), "Weapon Quality: " + str(self.quality), "Weapon Type: " +
               self.weaponType))

    # Show data of given weapon
    def show_weapon_data(self):
        wData = get_weapon_data(self.typeID)
        wAttr = get_table_data('TypeOfWeapon')
        for i in range(len(wData)):
            print(str(wAttr[i][1]) + ': ' + str(wData[i]))


class Enemy(object):
    def __init__(self, enemyID, initiative, HP, strength, endurance, durability, agility, accuracy):
        self.enemyID = enemyID
        self.stats = [initiative, HP, strength, endurance, durability, agility, accuracy]
        self.currInitiative = self.stats[0]
        self.damage = 0
        self.durability = self.stats[4]
        self.defending = False

    # Check if enemy is dead
    def check_living(self):
        return self.stats[1] > 0

    # Enable guard mode, guard mode raises defense and makes damage = 0
    def enable_guard(self, currWeapon):
        self.defending = True
        if currWeapon != 0:
            weaponData = get_weapon_data(currWeapon)
            weaponQuality = get_weapon_quality(currWeapon)
            self.durability = self.stats[DURABILITY] + ((weaponData[WEAPON_DURABILITY] + weaponQuality) / 10)
            self.damage = 0
        else:
            print("No guarding cuz currWeapon is 0")
            self.durability = self.stats[DURABILITY]

    # Disable guard mode
    def disable_guard(self):
        self.durability = self.stats[DURABILITY]

    # Set the attack damage
    def attack(self, currWeapon):
        if currWeapon != 0:
            weaponQuality = get_weapon_quality(currWeapon)
            weaponData = get_weapon_data(currWeapon)
            self.damage = weaponData[WEAPON_DAMAGE] + (weaponQuality + self.stats[2]) / 10
        else:
            self.damage = self.stats[2]


class Character(object):
    def __init__(self, charID, name, level, initiative, HP, strength, endurance, durability, agility, accuracy,
                 inventoryCap, freePoints, exp, corruption, stress, progress):
        self.charID = charID
        self.name = name
        self.level = level
        self.stress = stress
        self.data = [initiative, HP, strength, endurance, durability, agility, accuracy, inventoryCap]
        self.stats = self.data
        self.freePoints = freePoints
        self.freeInventory = inventoryCap
        self.usedInventory = []
        self.corruption = corruption
        self.exp = exp
        self.progress = progress
        self.currInitiative = self.data[INITIATIVE]
        self.damage = 0
        self.durability = self.data[DURABILITY]
        self.defending = False

    # Check if character is alive
    def check_living(self):
        return self.stats[1] > 0

    # Check character stats
    def check_stats(self):
        for i in range(len(self.data)):
            statVal = self.data[i] - math.trunc(math.sqrt(self.stress))
            self.stats[i] = statVal

    # Fill the inventory with the data of the selected weapon
    def fill_inventory(self, weaponID, typeID, weaponType, weaponQuality):
        newWeapon = Weapon(weaponID, typeID, weaponType, weaponQuality)
        self.usedInventory.append(newWeapon)
        self.freeInventory -= newWeapon.size

    # Find the weapon in the inventory given the weapon ID, return 0 if you can't find it
    def find_weapon(self, weaponID):
        for weapon in self.usedInventory:
            if weapon.wID == weaponID:
                return weapon
        return 0

    # remove a weapon from the inventory given the weapon id
    def remove_inventory(self, weaponID):
        weapon = self.find_weapon(weaponID)
        if weapon == 0:
            print("You own no such weapon")
            return
        self.usedInventory.remove(weapon)

    # Check if the weapon given is still usable
    def check_weapon_usability(self, weaponID):
        weapon = self.find_weapon(weaponID)
        if weapon.quality == 0:
            discard = input("This weapon is broken. Do you want to discard this weapon? Enter " +
                            BUTTON + " to do so: ")
            if discard == BUTTON:
                self.remove_inventory(weaponID)
        return weapon.quality < 0

    # Damage the weapon due to usage
    def damage_weapon(self, weaponID):
        weapon = self.find_weapon(weaponID)
        if weapon == 0:
            return
        weapon.lower_quality()

    # get the list of weapons in inventory
    def get_weapon_list(self):
        weaponList = []
        for weapon in self.usedInventory:
            weaponList.append(weapon.wID)
        return weaponList

    # Show everything in the inventory and show each weapon in the inventory
    def show_inventory(self):
        skip_line(2)
        displayingData = True
        while displayingData:
            for weapon in self.usedInventory:
                weapon.display_weapon()
                skip_line(1)
            try:
                weaponID = int(input("Select an appropriate weapon id to view its data, or "
                                     "enter a letter to continue: "))
                skip_line(1)
                weaponList = self.get_weapon_list()
                while weaponID not in weaponList:
                    weaponID = int(input("Please select an appropriate id as listed above: "))
                weapon = self.find_weapon(weaponID)
                weapon.show_weapon_data()
                time.sleep(WAIT_TIME)
                skip_line(2)
            except ValueError:
                return

    # Level up the character if possible
    def ascend(self):
        skip_line(5)
        self.level += 1
        self.freePoints += ASC_POINTS
        self.exp = self.exp - ASC_EXP
        print("You have ascended! You are now Level " + str(self.level))
        skip_line(5)

    # Customize your character
    def customize(self):
        print("Customizing your character, you may exit at any moment by inputting a non integer.")
        pt = self.freePoints
        for i, attr in enumerate(BASE_STATS[0]):
            print("You have " + str(pt) + " points left. \n")
            try:
                val = int(input(attr + ": "))
                while val > pt:
                    try:
                        val = int(input("There's not enough points. You only have " + str(pt) +
                                        " points. Please reenter: "))
                    except ValueError:
                        return
                pt -= val
                self.data[i] += val
                self.freePoints = pt
                if pt <= 0:
                    self.check_stats()
                    return
            except ValueError:
                self.check_stats()
                return

    # Show character stats
    def show_stats(self):
        skip_line(2)
        print("Name: " + self.name)
        skip_line(1)
        print("Level: " + str(self.level))
        print("Exp: " + str(self.exp))
        print("Corruption: " + str(self.corruption))
        print("Stress: " + str(self.stress))
        skip_line(1)
        for i, attr in enumerate(BASE_STATS[0]):
            print(attr + ": " + str(self.data[i]) + "   [" + str(self.stats[i]) + "]")
        skip_line(1)
        print("Free points to distribute: " + str(self.freePoints))
        time.sleep(WAIT_TIME)
        skip_line(2)

    # Update the character to database
    def save_character(self):
        if in_database(self.charID):
            update_character(self)
        else:
            insert_character(self)
        weaponList = get_weapon_id_list()
        for i in range(len(weaponList)):
            weaponList[i] = weaponList[i][0]
        for weapon in self.usedInventory:
            if weapon.wID not in weaponList:
                update_weapons(weapon.wID, weapon.quality, self.charID, weapon.typeID)
            else:
                update_quality(weapon.quality, weapon.wID)

    # Increase character corruption
    def corrupt(self, choice):
        val = check_corruption(choice)
        diff = abs(val - self.corruption)
        if diff > CORRUPTION_DIFFERENCE:
            self.stress += 1
        self.corruption += CORRUPTION_INCREASE

    # Enable guard mode
    def enable_guard(self, currWeapon):
        self.defending = True
        if currWeapon != 0:
            weapon = self.find_weapon(currWeapon)
            weaponData = get_weapon_data(currWeapon)
            self.durability = self.stats[DURABILITY] + (weaponData[WEAPON_DURABILITY] + weapon.quality) / 10
        else:
            self.durability = self.stats[DURABILITY]
        self.damage = 0

    # Disable guard mode
    def disable_guard(self):
        self.defending = False
        self.durability = self.stats[DURABILITY]

    # Set attack damage in accordance to weapon damage
    def attack(self, currWeapon):
        if currWeapon != 0:
            weapon = self.find_weapon(currWeapon)
            weaponData = get_weapon_data(currWeapon)
            self.damage = weaponData[WEAPON_DAMAGE] + (weapon.quality + self.stats[2]) / 10
        else:
            self.damage = self.stats[STRENGTH]

    # Reset player initiative
    def reset_initiative(self):
        self.currInitiative = self.stats[INITIATIVE]
