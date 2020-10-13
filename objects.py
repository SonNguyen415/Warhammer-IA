from dataFetching import *


class Characters(object):
    def __init__(self, name, level, strength, endurance, durability, agility, accuracy, inventoryCap, freePoints):
        self.name = name
        self.level = level
        self.data = [strength, endurance, durability, agility, accuracy, inventoryCap]
        self.freePoints = freePoints
        self.freeInventory = inventoryCap
        self.weaponList = []

    def fill_inventory(self, weaponID, typeID):
        newWeapon = [weaponID, typeID]
        self.weaponList.append(newWeapon)
        self.freeInventory -= get_weapon_size(weaponID)

    def ascend(self):
        self.level += 1
        self.freePoints += ASC_POINTS

    def change_stats(self, val, x):
        self.data[x] += val

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

    def show_stats(self):
        print(self.name)
        for i, attr in enumerate(BASE_STATS[0]):
            print(attr + ": " + str(self.data[i]) + "\n")


class Weapon(object):
    def __init__(self, quality, name="No Name"):
        self.name = name
        self.quality = quality

    def maintain_weapon(self):
        self.quality += 1

    def damage_weapon(self):
        self.quality -= 1
