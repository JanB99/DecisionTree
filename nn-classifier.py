import tensorflow as tf
import csv
import numpy as np

with open("dataset.csv", "r") as file:
    reader = csv.reader(file)
    data = [row for row in reader]
    headers = data[0]
    del data[0]


def dict(rows, i):
    counts = {}
    n = 0
    for row in rows:
        if row[i] not in counts:
            counts[row[i]] = n
            n += 1
        # counts[row[index]] += 1
    # counts = {k: v/len(rows) for (k, v) in counts.items()}
    return counts


def transform_data(rows, t_table):

    labels = []

    for i, row in enumerate(rows):
        labels.append(i)
        del rows[i][-1]
        for j, val in enumerate(row):
            head = headers[j]
            if head == "label":
                continue
            rows[i][j] = t_table[head][val]

    return np.array(rows), np.array(labels)


translation_table = {}
for index, header in enumerate(headers):
    translation_table[header] = dict(data, index)
    # print(header, translation_table[header])


# print(translation_table)


x_train, y_train = transform_data(data, translation_table)

print(x_train)
print(y_train)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(16, input_shape=(9, ), activation='relu'))
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(24, activation=tf.nn.softmax))

model.compile(optimizer="adam", loss=tf.losses.sparse_categorical_crossentropy)

model.fit(x_train, y_train, epochs=5)

print(x_train[0])

prediction = model.predict(np.array(x_train[0]).reshape((9, )))
print(prediction)