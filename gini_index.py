import csv

with open("dataset.csv", "r") as file:
    reader = csv.reader(file)
    data = [row for row in reader]
    headers = data[0]
    del data[0]


def gini(rows, index):
    counts = {}
    for row in rows:
        if row[index] not in counts:
            counts[row[index]] = 0
        counts[row[index]] += 1
    counts = {k: v/len(rows) for (k, v) in counts.items()}

    impurity = 1
    for (k, v) in counts.items():
        impurity -= v**2
    return impurity, counts


for i in range(len(headers)):
    print(headers[i], gini(data, i))
