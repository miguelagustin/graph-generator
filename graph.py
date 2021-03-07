import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import pathlib

current_path = str(pathlib.Path(__file__).parent.absolute())

directories = [fr"{current_path}\r1", fr"{current_path}\r2", fr"{current_path}\r3"]


def count(row):
    for rows in row:
        if rows[0] in ['big_enemy_hit', 'small_enemy_hit']:
            if rows[0] == 'big_enemy_hit':
                return 'big'
            elif rows[0] == 'small_enemy_hit':
                return 'small'
    return 'none'


big = [0 for x in range(6)]
small = [0 for x in range(6)]
none = [0 for x in range(6)]


def do_the_thing(row, index):
    result = count(row)
    if result == 'big':
        big[index] += 1
    if result == 'small':
        small[index] += 1
    if result == 'none':
        none[index] += 1


def do_the_graph():
    labels = ['0-20', '20-40', '40-60', '60-80', '80-100', '100-120']
    small_percentage = [x * 100 / (big[index] + small[index] + none[index]) for index, x in enumerate(small)]
    big_percentage = [x * 100 / (big[index] + small[index] + none[index]) for index, x in enumerate(big)]
    new_list = [abs(x1 - x2) for (x1, x2) in zip(small_percentage, big_percentage)]
    print(new_list)
    print(big_percentage)
    print(small_percentage)
    N = len(labels)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    # p1 = plt.bar(ind, big_percentage, width,zorder=2)
    # p2 = plt.bar(ind, small_percentage, width, zorder=1)
    colors = ['C0', 'C1']
    fig, ax = plt.subplots()

    for x, ha, hb in zip(ind, small_percentage, big_percentage):
        for i, (h, c) in enumerate(sorted(zip([ha, hb], colors))):
            plt.bar(x, h, color=c, zorder=-i)

    axis_font = {'fontname': 'Arial', 'size': '14'}
    plt.ylabel('Percentage', **axis_font)
    plt.xlabel('Time (seconds)', **axis_font)
    plt.xticks(ind, labels)
    plt.legend(('Small', 'Big'))
    plt.show()


for directory in directories:
    for csv_file in os.listdir(directory):
        try:
            filename = os.path.join(directory, csv_file)
            if "csv" in filename:
                rows = []

                with open(filename, 'r') as file:
                    reader = csv.reader(file, delimiter=',')
                    next(reader)  # skip the first row
                    for row in reader:
                        rows.append([row[0].strip(), float(row[1]), row[2]])
                row_list = [list() for _ in range(6)]
                for row in sorted(rows, key=lambda x: -x[1]):
                    if 0 <= row[1] < 20:
                        row_list[0].append(row)
                    if 20 <= row[1] < 40:
                        row_list[1].append(row)
                    if 40 <= row[1] < 60:
                        row_list[2].append(row)
                    if 60 <= row[1] < 80:
                        row_list[3].append(row)
                    if 80 <= row[1] < 100:
                        row_list[4].append(row)
                    if 100 <= row[1] < 120:
                        row_list[5].append(row)
                for index, x in enumerate(row_list):
                    do_the_thing(x, index)

                else:
                    pass
        except EnvironmentError:
            print('File not found!')

do_the_graph()
