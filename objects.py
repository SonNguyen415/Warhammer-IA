from dataFetching import *


class Characters(object):
    def __init__(self, charID, name, level, strength, endurance, durability, agility, accuracy, inventoryCap, freePoints):
        self.charID = charID
        self.name = name
        self.level = level
        self.data = [strength, endurance, durability, agility, accuracy, inventoryCap]
        self.freePoints = freePoints
        self.freeInventory = inventoryCap
        self.weaponList = []

    # Fill the inventory with the data of the selected weapon
    def fill_inventory(self, weaponID, typeID):
        quality = 5
        newWeapon = Weapon(weaponID, quality, typeID)
        self.weaponList.append(newWeapon)
        self.freeInventory -= get_weapon_size(weaponID)

    # Level up the character
    def ascend(self):
        self.level += 1
        self.freePoints += ASC_POINTS

    # Change stats of a given attribute
    def change_stats(self, val, x):
        self.data[x] += val

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
                self.change_stats(val, i)
                self.freePoints = pt
                if pt <= 0:
                    return
            except ValueError:
                return

    # Show character stats
    def show_stats(self):
        print("Name: " + self.name)
        skip_line(1)
        for i, attr in enumerate(BASE_STATS[0]):
            print(attr + ": " + str(self.data[i]) + "\n")


class Weapon(object):
    def __init__(self, wID, quality, typeID):
        self.wID = wID
        self.quality = quality
        self.typeID = typeID
    
    # Get the maximum possible quality of the current weapon
    def get_max_quality(self):
        return 1

    # Improve weapon quality each time you maintain it
    def maintain_weapon(self):
        self.quality += 1
        if self.quality >= self.get_max_quality():
            print("You've maximized the reliability of this weapon.")
            self.quality = self.get_max_quality()

    # Damage the weapons due to use
    def damage_weapon(self):
        self.quality -= 2
        if self.quality <= 0:
            print("This weapon is now broken.")
            self.quality = 0
   
