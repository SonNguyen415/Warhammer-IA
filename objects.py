from dataFetching import *


class Weapon(object):
    def __init__(self, wID, typeID):
        self.wID = wID
        self.typeID = typeID
        self.maxQuality = get_weapon_quality(typeID)
        self.quality = self.maxQuality
        self.size = get_weapon_size(typeID)

        # Improve weapon quality each time you maintain it
    def maintain_weapon(self):
        self.quality += 1
        if self.quality >= self.maxQuality:
            print("You've maximized the reliability of this weapon.")
            self.quality = self.maxQuality

    # Damage the weapons due to use
    def damage_weapon(self):
        self.quality -= 2
        if self.quality <= 0:
            print("This weapon is now broken.")
            self.quality = 0

    # Show weapon data
    def show_weapon(self):
        print(self.typeID)


class Character(object):
    def __init__(self, charID, name, level, strength, endurance, durability, agility, accuracy, inventoryCap, freePoints):
        self.charID = charID
        self.name = name
        self.level = level
        self.data = [strength, endurance, durability, agility, accuracy, inventoryCap]
        self.freePoints = freePoints
        self.freeInventory = inventoryCap
        self.usedInventory = []

    # Fill the inventory with the data of the selected weapon
    def fill_inventory(self, weaponID, typeID):
        newWeapon = Weapon(weaponID, typeID)
        self.usedInventory.append(newWeapon)
        self.freeInventory -= newWeapon.size

    # Level up the character
    def ascend(self):
        self.level += 1
        self.freePoints += ASC_POINTS

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
        print("Name: " + self.name)
        skip_line(1)
        for i, attr in enumerate(BASE_STATS[0]):
            print(attr + ": " + str(self.data[i]) + "\n")

    # Update the character
    def save_character(self):
        if not_in_database(self.charID):
            insert_character(self.charID, self.name, self.level, self.data, self.freePoints)
        else:
            update_character(self.charID, self.level, self.data, self.freePoints)
        for weapon in self.usedInventory:
            update_weapons(weapon.wID, weapon.quality, self.charID, weapon.typeID)