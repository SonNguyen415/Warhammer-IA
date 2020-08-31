class TreeNode(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def get_next(self):
        return self.children[0]

    def tree_travel(self):
        spaces = "  "
        if self.children:
            print(self.data)
            for child in self.children:
                print(spaces + child.data)
            choice = input('Select your choices: ')
            for child in self.children:
                if str(child.data).lower() == choice.lower():
                    nextScene = child.get_next()
                    nextScene.tree_travel()
        else:
            return


def build_product_tree():
    root = TreeNode("Intro")

    choice1a = TreeNode("Choice 1a")
    choice2a = TreeNode("Choice 2a")

    scene1a = TreeNode("Scene 1a")
    scene2a = TreeNode("Scene 2a")
    scene3a = TreeNode("Scene 3a")
    scene4a = TreeNode("Scene 4a")

    choice1b = TreeNode("Choice 1b")
    choice2b = TreeNode("Choice 2b")
    choice3b = TreeNode("Choice 3b")
    choice4b = TreeNode("Choice 4b")
    choice5b = TreeNode("Choice 5b")
    choice6b = TreeNode("Choice 6b")
    choice7b = TreeNode("Choice 7b")
    choice8b = TreeNode("Choice 8b")

    scene1b = TreeNode("Scene 1b")
    scene2b = TreeNode("Scene 2b")
    scene3b = TreeNode("Scene 3b")
    scene4b = TreeNode("Scene 4b")
    scene5b = TreeNode("Scene 5b")
    scene6b = TreeNode("Scene 6b")
    scene7b = TreeNode("Scene 7b")
    scene8b = TreeNode("Scene 8b")

    root.add_child(choice1a)
    root.add_child(choice2a)

    choice1a.add_child(scene1a)
    choice1a.add_child(scene2a)
    choice2a.add_child(scene3a)
    choice2a.add_child(scene4a)

    scene1a.add_child(choice1b)
    scene1a.add_child(choice2b)
    scene2a.add_child(choice3b)
    scene2a.add_child(choice4b)
    scene3a.add_child(choice5b)
    scene3a.add_child(choice6b)
    scene4a.add_child(choice7b)
    scene4a.add_child(choice8b)

    choice1b.add_child(scene1b)
    choice2b.add_child(scene2b)
    choice3b.add_child(scene3b)
    choice4b.add_child(scene4b)
    choice5b.add_child(scene5b)
    choice6b.add_child(scene6b)
    choice7b.add_child(scene7b)
    choice8b.add_child(scene8b)

    return root


myTree = build_product_tree()
myTree.tree_travel()