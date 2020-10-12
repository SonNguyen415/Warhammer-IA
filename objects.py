from dataFetching import *


class Characters(object):
    def __init__(self, name, level, strength, endurance, durability, agility, accuracy, inventoryCap, freePoints):
        self.name = name
        self.level = level
        self.data = [strength, endurance, durability, agility, accuracy]
        self.freePoints = freePoints
        self.inventory = inventoryCap

    def fill_inventory(self, objSize):
        self.inventory -= objSize

    def ascend(self):
        self.level += 1
        self.freePoints += ASC_POINTS

    def change_stats(self, val, x):
        self.data[x] += val

    def set_free_points(self, pt):
        self.freePoints = pt

    def customize(self):
        print("Customizing your character, you may exit at any moment by inputting a non integer.")
        pt = self.freePoints()
        for i,attr in enumerate(BASE_STATS[0]):
            print("You have " + str(pt) + " points left. \n")
            try:
                val = int(input(attr + ": "))
                while val > pt:
                    val = int(
                        input("There's not enough points. You only have " + str(pt) + " points. Please reenter: "))
                pt -= val
                self.change_stats(val, i)
                self.freePoints = pt
                if pt <= 0:
                    return
            except ValueError:
                return
