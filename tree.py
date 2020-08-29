class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


root = Node(0)
a = Node(1)
b = Node(2)
c = Node(3)

root.add_child(a)
root.add_child(b)
root.children
for each in root.children:
    print(each.data)

