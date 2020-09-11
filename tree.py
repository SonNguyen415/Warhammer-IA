from random import *
from type import * 
from switcher import *

class TreeNode(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 1
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def get_next_scene(self):
        n = randint(0, len(self.children)-1)
        return self.children[n]


    def tree_travel(self):
        spaces = "  "
        if self.children:
            print(self.data)
            for child in self.children:
                print(spaces + child.data)
            choice = int(input('Select your choices: '))
            chosen = self.children[choice-1]
            delay_print(chosen.data)
            nextScene = chosen.get_next_scene()
            nextScene.tree_travel()
        else:
            return

def build_product_tree():

    root = TreeNode(S01content)

    nCA1 = TreeNode(CA1content)
    nCA2 = TreeNode(CA2content)

    nSA1 = TreeNode(SA1content)
    nSA2 = TreeNode(SA2content)
    nSA3 = TreeNode(SA3content)
    nSA4 = TreeNode(SA4content)

    root.add_child(nCA1)
    root.add_child(nCA2)

    nCA1.add_child(nSA1)
    nCA1.add_child(nSA2)
    nCA2.add_child(nSA3)
    nCA2.add_child(nSA4)

    return root



