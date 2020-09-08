from content import *
from random import *

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
            print(chosen.data)
            nextScene = chosen.get_next_scene()
            print(nextScene.data)
            nextScene.tree_travel()
        else:
            return

def build_product_tree():

    root = TreeNode(S1Acontent)

    nC1A = TreeNode(C1Acontent)
    nC1B = TreeNode(C1Bcontent)

    nS2A = TreeNode(S2Acontent)
    nS2B = TreeNode(S2Bcontent)
    nS2C = TreeNode(S2Ccontent)
    nS2D = TreeNode(S2Dcontent)

    root.add_child(nC1A)
    root.add_child(nC1B)

    nC1A.add_child(nS2A)
    nC1A.add_child(nS2B)
    nC1B.add_child(nS2C)
    nC1B.add_child(nS2D)

    return root


myTree = build_product_tree()
myTree.tree_travel()