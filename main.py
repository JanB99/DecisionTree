import csv
import math


class Question:
    def __init__(self, col, value):
        self.column = col
        self.value = value

    def match(self, example):
        value = example[self.column]
        if self.is_int():
            return value >= self.value
        else:
            return value == self.value

    def match_value(self, value):
        if self.is_int():
            return float(value) >= self.value
        else:
            return value == self.value

    def is_int(self):
        return isinstance(self.value, int) or isinstance(self.value, float)

    def __repr__(self):
        return "is {} {} {}?".format(headers[self.column], ">=" if self.is_int() else "==", self.value)


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)

    return true_rows, false_rows


def count_classes(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def gini(rows):
    counts = count_classes(rows)
    impurity = 1
    for label in counts:
        prob = counts[label] / float(len(rows))
        impurity -= prob**2
    return impurity


def information_gain(current, left, right):
    #een aangepaste manier om de mate aan chaos/onzekerheid te meten. normaal gesproken word deze gemeten met de log2 ipv de gini
    #gini is ook een methode om disorder te meten
    p = len(left) / (len(left) + len(right))
    return current - p * gini(left) - (1-p) * gini(right)


def find_best_question(rows):
    best_question = None
    best_gain = 0
    current = gini(rows)

    num_features = len(rows[0])-1

    for col in range(num_features):

        values = {row[col] for row in rows}

        for value in values:

            question = Question(col, value)

            true, false = partition(rows, question)

            info_gain = information_gain(current, true, false)
            # print(question)
            # print(info_gain)

            if info_gain > best_gain:
                best_gain = info_gain
                best_question = question

    return best_gain, best_question


class Node:
    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

    def print(self, spacing, boolean):
        print(spacing, ">", self.question)
        self.true_branch.print(spacing+"  ", True)
        self.false_branch.print(spacing+"  ", False)


class Leaf:
    def __init__(self, rows):
        self.predictions = count_classes(rows)
        total_counts = sum(self.predictions.values())
        self.probabilities = {key: value / total_counts for (key, value) in self.predictions.items()}

    def print(self, spacing, boolean):
        print(spacing, str(boolean) + "-->", self.probabilities)


class Tree:
    def __init__(self, rows):
        self.root = self.create_tree(rows)

    def create_tree(self, rows):

        gain, question = find_best_question(rows)
        if gain == 0:
            return Leaf(rows)
        true_rows, false_rows = partition(rows, question)

        true_branch = self.create_tree(true_rows)
        false_branch = self.create_tree(false_rows)
        return Node(question, true_branch, false_branch)

    def print_tree(self):
        self.root.print("", "")
        print("\n")

    def predict(self, row, node):

        if isinstance(node, Leaf):
            print(node.probabilities)
            return

        if node.question.match(row):
            self.predict(row, node.true_branch)
        else:
            self.predict(row, node.false_branch)


with open("dataset.csv", 'r', newline='') as file:
    reader = csv.reader(file)
    dataset = [row for (index, row) in enumerate(reader)]
    headers = dataset[0]
    del dataset[0]

# headers = ["haircolor", "job", "gender", "age", "label"]
#
# dataset = [
#     ["black", "musician", "male", 50, "Micheal Jackson"],
#     ["grey", "scientist", "male", 76, "Albert Einstein"],
#     ["n/a", "comedian", "male", 53, "Joe Rogan"],
#     ["blonde", "musician", "female", 43, "Shakira"],
#     ["blonde", "musician", "female", 50, "Gwen Stefani"],
#     ["black", "coder", "male", 21, "Jan Baljan"],
#     ["black", "fighter", "male", 35, "Nate Diaz"],
#     ["black", "fighter", "male", 35, "Jorge Masvidal"],
#     ["grey", "comedian", "male", 60, "Joey Diaz"],
#     ["black", "scientist", "male", 36, "Lex Fridman"],
#     ["black", "musician", "female", 39, "Beyonce"],
#     ["brown", "musician", "female", 18, "Billie Eilish"],
#     ["blonde", "bodybuilder", "male", 23, "Stan Deckers"],
# ]
#
# test = [
#     ["", "", "male", 50, "Micheal Jackson"],
#     ["grey", "scientist", "male", 76, "еуые2"],
# ]

# headers = ["color", "diameter", "label"]
#
# dataset = [
#     ['Green', 3, 'Apple'],
#     ['Yellow', 3, 'Apple'],
#     ['Red', 1, 'Grape'],
#     ['Red', 1, 'Grape'],
#     ['Yellow', 3, 'Lemon'],
# ]

tree = Tree(dataset)

tree.print_tree()

# tree.predict(test[0], tree.root)


def ask(root):

    if isinstance(root, Leaf):
        print("\n", root.probabilities)
        return

    print(root.question)

    answer = bool(int(input("input (True, 1 or False, 0): ")))

    if answer:
        ask(root.true_branch)
    else:
        ask(root.false_branch)


# ask(tree.root)

