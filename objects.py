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
        print(("Weapon ID: " + str(self.typeID), "Weapon Quality: " + str(self.quality), "Weapon Type: " +
               self.weaponType))

    # Show data of given weapon
    def show_weapon_data(self):
        wData = get_weapon_data(self.wID)
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

    # Damage enemy
    def wound(self, damage):
        self.stats[1] -= damage

    # Check if enemy is dead
    def check_living(self):
        return self.stats[1] > 0

    def attack(self):
        self.damage = self.stats[2] + 10

    def guard(self, currWeapon):
        self.defending = True
        if currWeapon != 0:
            weaponData = get_weapon_data(currWeapon)
            weaponQuality = get_weapon_quality(currWeapon)
            self.durability = self.stats[4] + ((weaponData[WEAPON_DURABILITY] + weaponQuality) / 10)
            self.damage = 0
        else:
            self.durability = self.stats[4]

    def unguard(self):
        self.durability = self.stats[4]

    def attack(self, currWeapon):
        if currWeapon != 0:
            weaponQuality = get_weapon_quality(currWeapon)
            weaponData = get_weapon_data(currWeapon)
            self.damage = weaponData[WEAPON_DAMAGE] + (weaponQuality + self.stats[2]) / 10
        else:
            self.damage = self.stats[2]


class Character(object):
    def __init__(self, charID, name, level, initiative, HP, strength, endurance, durability, agility, accuracy,
                 inventoryCap, freePoints, exp, corruption, stress):
        self.charID = charID
        self.name = name
        self.level = level
        self.stress = stress
        self.data = [initiative, HP, strength, endurance, durability, agility, accuracy, inventoryCap]
        self.stats = []
        self.freePoints = freePoints
        self.freeInventory = inventoryCap
        self.usedInventory = []
        self.corruption = corruption
        self.exp = exp
        self.check_stats()
        self.currInitiative = self.data[0]
        self.damage = 0
        self.durability = self.data[4]
        self.defending = False

    # Kill character
    def kill(self):
        self.stats[1] = 0

    # Wound character
    def wound(self, damage):
        self.stats[1] -= damage

    # Check if character is alive
    def check_living(self):
        return self.stats[1] > 0

    # Check character stats
    def check_stats(self):
        for attr in self.data:
            self.stats.append(attr - math.trunc(math.sqrt(self.stress)))

    # Fill the inventory with the data of the selected weapon
    def fill_inventory(self, weaponID, typeID, weaponType, weaponQuality):
        newWeapon = Weapon(weaponID, typeID, weaponType, weaponQuality)
        self.usedInventory.append(newWeapon)
        self.freeInventory -= newWeapon.size

    def find_weapon(self, weaponID):
        for weapon in self.usedInventory:
            if weapon.wID == weaponID:
                return weapon
        return 0

    def remove_inventory(self, weaponID):
        weapon = self.find_weapon(weaponID)
        if weapon == 0:
            print("You own no such weapon")
            return
        self.usedInventory.remove(weapon)

    def check_weapon_usability(self, weaponID):
        weapon = self.find_weapon(weaponID)
        if weapon == 0:
            return
        if weapon.quality == 0:
            discard = input("This weapon is broken. Do you want to discard this weapon? Enter " +
                            BUTTON + " to do so: ")
            if discard == BUTTON:
                self.remove_inventory(weaponID)
        return weapon.quality > 0

    def damage_weapon(self, weaponID):
        weapon = self.find_weapon(weaponID)
        if weapon == 0:
            return
        weapon.lower_quality()

    # Show everything in the inventory and show each weapon in the inventory
    def show_inventory(self):
        skip_line(2)
        displayingData = True
        while displayingData:
            for weapon in self.usedInventory:
                weapon.display_weapon()
                skip_line(1)
            try:
                wIndex = int(input("Select an appropriate weapon id to view its data, or "
                                   "enter a letter to continue: ")) - 1
                skip_line(1)
                while wIndex < 0 or wIndex >= len(self.usedInventory):
                    wIndex = int(input("Please select an appropriate id as listed above: ")) - 1
                weapon = self.usedInventory[wIndex]
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
                    return
            except ValueError:
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
            print(attr + ": " + str(self.data[i]))
        skip_line(1)
        print("Free points to distribute: " + str(self.freePoints))
        time.sleep(WAIT_TIME)
        skip_line(2)

    # Update the character
    def save_character(self):
        if not_in_database(self.charID):
            insert_character(self.charID, self.name, self.level, self.data, self.freePoints,
                             self.corruption, self.exp, self.stress)
        else:
            update_character(self.charID, self.level, self.data, self.freePoints,
                             self.corruption, self.exp, self.stress)
        for weapon in self.usedInventory:
            update_weapons(weapon.wID, weapon.quality, self.charID, weapon.typeID)

    # Increase character corruption
    def corrupt(self, choice):
        val = check_corruption(choice)
        diff = abs(val - self.corruption)
        if diff > CORRUPTION_DIFFERENCE:
            self.stress += 1
        self.corruption += CORRUPTION_INCREASE

    def guard(self, currWeapon):
        self.defending = True
        if currWeapon != 0:
            weapon = self.find_weapon(currWeapon)
            weaponData = get_weapon_data(currWeapon)
            self.durability = self.stats[4] + (weaponData[WEAPON_DURABILITY] + weapon.quality) / 10
        else:
            self.durability = self.stats[4]
        self.damage = 0

    def unguard(self):
        self.defending = False
        self.durability = self.stats[4]

    def attack(self, currWeapon):
        if currWeapon != 0:
            weapon = self.find_weapon(currWeapon)
            weaponData = get_weapon_data(currWeapon)
            self.damage = weaponData[WEAPON_DAMAGE] + (weapon.quality + self.stats[2]) / 10
        else:
            self.damage = self.stats[2]

    def reset_initiative(self):
        self.currInitiative = self.stats[0]
