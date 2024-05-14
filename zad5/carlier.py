# Carlier

from operator import itemgetter
import copy
import timeit
import time

time_limit = 0.2

import heapq

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        # Item is a tuple (LB, problem_state)
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def is_empty(self):
        return len(self.heap) == 0


class PriorityQueue:

    def __init__(self, key, rev, l):
        self._key = key
        self._rev = rev
        if len(l) == 0:
            self._list = []
        else:
            self._list = l.sort(key=key, reverse=rev)

    def delete(self):
        self._list.pop(len(self._list)-1)

    def add(self, val):
        self._list.append(val)
        self._list.sort(key=self._key, reverse=self._rev)
        # print(f"key = {self._key}, list = {self._list}")

    def display(self):
        print(self._list)

    def return_list(self):
        return self._list

    def is_empty(self):
        if len(self._list) == 0:
            return True
        else:
            return False

    def get_element(self):
        return self._list[len(self._list)-1]

    def get_r(self, nb):
        # print("r getted")
        return self._list[len(self._list)-1][0]

def read(nb):
    lst = []
    with open('data/SCHRAGE' + str(nb) + '.DAT') as f:
        f.readline() #pominięcie n
        for i in f:
            x, y, z = i.split()
            lst.append([int(x), int(y), int(z)])
    return sorted(lst, key=lambda i: i[0]) # sortowanie po r

def get_anwser(nb):
    return 0
    with open('data/CARLIER' + str(nb) + '.OUT') as f:
        x = f.readline() #pominięcie n
    return x

def schrage(data):
    t = 0
    k = 0
    b = 0 # indeks zadania z cmaxem w permutacji
    N = PriorityQueue(itemgetter(0), True, []) # niegotowe
    G = PriorityQueue(itemgetter(2), False, []) # gotowe

    C_max = 0
    pi = []

    for i in range(0, len(data)):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2])])

    while G.is_empty() is False or N.is_empty() is False:  # 2
        while N.is_empty() is False and int(N.get_r(0)) <= t:  # 3
            e = N.get_element()
            G.add(e)
            N.delete()
        if G.is_empty() is True:                                     # 5
            t = int(N.get_r(0))                                    # 6
        else:
            e = G.get_element()
            G.delete()
            pi.append(e)
            t += int(e[1])
            if C_max <= int(t+int(e[2])):
                C_max = int(t+int(e[2]))
                b = k
            k += 1
            


    return pi,C_max,b

def schrage_div(data):
    '''
    Schringe, ale potrafi podzielić zadanie na części, jeżeli sie okaże, że pojawiło się zadanie gotowe do realizacji, które ma mniejszy czas stygnięcia niż aktualne zadanie na maszynie
    '''
    n = len(data)
    t = 0                                           # total time
    N = PriorityQueue(itemgetter(0), True, [])      # list of unordered tasks
    G = PriorityQueue(itemgetter(2), False, [])     # list of ready to implementation tasks

    C_max = 0
    pi = []
   

    for i in range(0, n):
        N.add([int(data[i][0]), int(data[i][1]), int(data[i][2])])

    onMachine=[0, 0, 999999]                    # current task initialization

    while G.is_empty() is False or N.is_empty() is False:   # check if at least one OR lists isn't empty
        while N.is_empty() is False and int(N.get_r(0)) <= t:  # check if N isn't empty AND availability time is less than total time
            e = N.get_element()                                # ready task
            G.add(e)
            N.delete()
            if e[2] > onMachine[2]:                            # check if time to complete ready task is higher than time on machine
                onMachine[1] = t - e[0]
                t = e[0]
                if onMachine[1] > 0:
                    G.add(onMachine)

        if G.is_empty() is True:                                     # 5
            t = int(N.get_r(0))                                    # 6
        else:
            e = G.get_element()
            G.delete()
            onMachine = e
            pi.append(e)
            t += int(e[1])
            C_max = max(C_max, int(t+int(e[2])))

        
        # Eliminacyjny test najwcześniejszego czasu rozpoczęcia (r)
        if not G.is_empty() and e[0] > t:
            # print("Eliminacja: zadanie nie może być rozpoczęte ze względu na zbyt późne 'r'")
            continue

        # Eliminacyjny test najpóźniejszego czasu zakończenia (q)
        if not G.is_empty() and e[2] < C_max - t:
            # print("Eliminacja: zadanie nie może być zakończone przed 'q'")
            continue


    return C_max

def findA(lst, b, Cmax):
    sum = a = 0
    for i in range(0, b + 1):
        sum += lst[i][1]

    while a < b and not Cmax == (lst[a][0] + lst[b][2] + sum):
        sum -= lst[a][1]
        a += 1
    return a

def findC(lst, a, b):
    for i in range(b - 1, a - 1, -1):
        if lst[i][2] < lst[b][2]:
            return i
    return None

def findRPQprim(lst, b, c):
    rprim = lst[c + 1][0]
    pprim = 0
    qprim = lst[c + 1][2]

    for i in range(c + 1, b + 1):
        if lst[i][0] < rprim:
            rprim = lst[i][0]
        if lst[i][2] < qprim:
            qprim = lst[i][2]
        pprim += lst[i][1]

    return rprim, pprim, qprim

def carlier(lst):
    global start_time
    heap = MinHeap()  # Inicjalizacja kopca
    initial_solution = schrage(copy.deepcopy(lst))
    # initial_lb = sum([task[1] for task in lst.values()])  # Prosty sposób na obliczenie LB
    initial_lb = schrage_div(copy.deepcopy(lst))  # Obliczenie LB za pomocą schrage_div
    heap.push((initial_lb, lst, initial_solution))

    best_Cmax = float('inf')

    while not heap.is_empty():
        if time.time() - start_time > time_limit:
            return best_Cmax  # Przekroczenie limitu czasu

        current_lb, _, current_solution = heap.pop()
        current_lst, Cmax, b = current_solution

        if current_lb >= best_Cmax:
            continue

        if Cmax < best_Cmax:
            best_Cmax = Cmax  # Aktualizacja najlepszego znalezionego rozwiązania

        a = findA(current_lst, b, Cmax)
        c = findC(current_lst, a, b)
        if c is None:
            continue  # Brak możliwości dalszego podziału

        rprim, pprim, qprim = findRPQprim(current_lst, b, c)

        # Tworzenie podproblemów
        # Podproblem dla zmodyfikowanego r
        modified_lst = copy.deepcopy(current_lst)
        modified_lst[c][0] = max(modified_lst[c][0], rprim + pprim)
        LB = schrage_div(copy.deepcopy(modified_lst))  # Ponowne obliczenie LB
        heap.push((LB, modified_lst, schrage(modified_lst)))

        # Podproblem dla zmodyfikowanego q
        modified_lst = copy.deepcopy(current_lst)
        modified_lst[c][2] = max(modified_lst[c][2], qprim + pprim)
        LB = schrage_div(copy.deepcopy(modified_lst))  # Ponowne obliczenie LB
        heap.push((LB, modified_lst, schrage(modified_lst)))

    return best_Cmax

if __name__ == "__main__":
    global start_time
    from data import data
    for x in data.values():
        start_time = time.time()
        result = carlier(x['tasks'])
        execution_time = time.time() - start_time
        print('Carlier: ' + str(result) +'\t| ' + 'Odp: '+ str(x['Cmax']) + '\t| Czas: ' + str(execution_time))




