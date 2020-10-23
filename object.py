from data import *


class Weapon(object):
    def __init__(self, wID, typeID, weaponType):
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
    def __init__(self, charID, name, level, HP, strength, endurance, durability, agility, accuracy, inventoryCap,
                 freePoints, corruption, exp, stress):
        self.charID = charID
        self.name = name
        self.level = level
        self.stress = stress
        self.data = [HP, strength, endurance, durability, agility, accuracy, inventoryCap]
        self.stats = []
        self.freePoints = freePoints
        self.freeInventory = inventoryCap
        self.usedInventory = []
        self.corruption = corruption
        self.exp = exp
        self.check_stats()

    def kill(self):
        self.stats[0] = 0

    def wound(self, damage):
        self.stats[0] -= damage

    def check_death(self):
        return self.stats[0] <= 0

    def check_stats(self):
        for attr in self.data:
            self.stats.append(attr - math.trunc(math.sqrt(self.stress)))

    # Fill the inventory with the data of the selected weapon
    def fill_inventory(self, weaponID, typeID, weaponType):
        newWeapon = Weapon(weaponID, typeID, weaponType)
        self.usedInventory.append(newWeapon)
        self.freeInventory -= newWeapon.size

    def show_inventory(self):
        print(self.usedInventory)
        for weapon in self.usedInventory:
            show_weapon_data(weapon.typeID)
            skip_line(2)

    # Level up the character if possible
    def ascend(self):
        if self.exp >= MAX_EXP:
            self.level += 1
            self.freePoints += ASC_POINTS
            self.exp = self.exp - MAX_EXP

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
        skip_line(1)
        for i, attr in enumerate(BASE_STATS[0]):
            print(attr + ": " + str(self.data[i]))
        skip_line(1)
        print("Corruption: " + str(self.corruption))
        print("Stress: " + str(self.stress))
        skip_line(1)
        print("Free points to distribute: " + str(self.freePoints))
        time.sleep(TIME_WAIT)
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

    def corrupt(self):
        val = check_corruption(self.charID)
        self.corruption += val


class Enemy(object):
    def __init__(self, HP, strength, endurance, durability, agility, accuracy):
        self.stats = [HP, strength, endurance, durability, agility, accuracy]

    def wound(self, damage):
        self.stats[0] -= damage

    def check_death(self):
        return self.stats[0] <= 0

    def reduce_durability(self, damage):
        self.stats[3] -= damage