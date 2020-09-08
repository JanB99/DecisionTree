class Node:
    def __init__(self, parent, left_child, right_child, value):
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.value = value

    def print(self):
        print(self.value)
        if (self.right_child is None) or (self.left_child is None):
            return
        self.left_child.print()
        self.right_child.print()


def create_nodes(k, parent):
    if k == 0:
        return

    n = Node(parent, None, None, k)

    n.left_child = create_nodes(k - 1, n)
    n.right_child = create_nodes(k - 1, n)

    return n


node = create_nodes(3, None)
node.print()
