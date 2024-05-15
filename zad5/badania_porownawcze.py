import carlier_plain
import carlier_eliminacje
import carlier_heap
import time

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    from data import data

    list_time = [list() for _ in range(3)] 

    for i, instance_data in list(data.items()):

        for j, carlier in enumerate([carlier_plain, carlier_eliminacje, carlier_heap]):
            start_time = time.time()
            carlier.carlier(instance_data['tasks'])
            end = time.time()
            time_d = end - start_time

            list_time[j].append(time_d)
            # print(i,j, list_time)

        print(i)

    x = np.arange(len(data.keys()))
    width = 0.2

    print(list_time)

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, list_time[0], width, label='Carlier')
    rects2 = ax.bar(x, list_time[1], width, label='Carlier eliminacje')
    rects3 = ax.bar(x + width, list_time[2], width, label='Carlier heap')


    ax.set_ylabel('Czas [s]')
    ax.set_title('Czas wykonania algorytmu Carlier')
    ax.set_xticks(x[::2])
    ax.set_xticklabels(list(data.keys())[::2])
    plt.xticks(rotation=45)
    ax.legend()

    fig.tight_layout()

    plt.yscale('log')

    plt.show()
        