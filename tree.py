from random import *
from type import * 
from switcher import *


# Tree object for game story
# Initialization and add_child courtesy of codebasics
class TreeNode(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    # Add a child to a parent node
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    # Get the level of the node, root is 1
    def get_level(self):
        level = 1
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    # Get the next scene from the choices, calculated based on character ability
    def get_next_scene(self):
        n = randint(0, len(self.children)-1)
        return self.children[n]

    # Travel to the next scene and display it and the choices available
    def tree_travel(self):
        if self.children:
            skip_line(2)
            print(self.data)
            for child in self.children:
                print(indent(2) + child.data)
            choice = int(input('Select your choices: '))
            chosen = self.children[choice-1]
            delay_print(chosen.data)
            nextScene = chosen.get_next_scene()
            nextScene.tree_travel()
        else:
            return


# Create tree, function setup courtesy of codebasics         
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



