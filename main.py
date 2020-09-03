
class Node:

    def __init__(self, parent, left_child, right_child, value):
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.value = value


def create_nodes(k, parent):
    if k == 0:
        return

    n = Node(parent, None, None, k)

    n.left_child = create_nodes(k - 1, n)
    n.right_child = create_nodes(k - 1, n)

    return n


def print_nodes(node):
    if node is None:
        return

    print(node.value)
    print_nodes(node.left_child)
    print_nodes(node.right_child)

# headers = ["haircolor", "job", "gender", "age", "label"]
#
# dataset = [
#     ["black", "musician", "male", 50, "Micheal Jackson"],
#     ["grey", "scientist", "male", 76, "Albert Einstein"],
#     ["n/a", "comedian", "male", 53, "Joe Rogan"],
#     ["blonde", "musician", "female", 43, "Shakira"],
# ]


node = create_nodes(3, None)
# print(node)

print_nodes(node)
