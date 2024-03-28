import neh_bez_akceleracji
import neh_akceleracja
import time

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = neh_akceleracja.read_data("neh.data.txt")

    list_time_bez_akc = []
    list_time_akc = []

    for i, instance_data in list(data.items()):

        start = time.time()
        neh_bez_akceleracji.neh(instance_data)
        end = time.time()
        time_bez_akc = end - start

        start = time.time()
        neh_akceleracja.neh(instance_data)
        end = time.time()
        time_akc = end - start

        list_time_bez_akc.append(time_bez_akc)
        list_time_akc.append(time_akc)

        print(i)

    x = np.arange(len(list_time_akc))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, list_time_bez_akc, width, label='Bez akceleracji')
    rects2 = ax.bar(x + width/2, list_time_akc, width, label='Z akceleracją')

    ax.set_ylabel('Czas [s]')
    ax.set_title('Czas wykonania algorytmu NEH')
    ax.set_xticks(x[::2])
    ax.set_xticklabels(list(data.keys())[::2])
    plt.xticks(rotation=45)
    ax.legend()

    fig.tight_layout()

    plt.show()
        