import time

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    data = {}
    while lines:
        line = lines.pop(0)
        if line.startswith("data."):
            data_name = line.split('data.')[1].strip(':\n')
            data[data_name] = {}
            i, k = map(int, lines.pop(0).split())
            data[data_name]["zadania"] = i
            data[data_name]["maszyny"] = k
            data[data_name]["tasks"] = {}
            for i in range(i):
                data[data_name]["tasks"][i+1] = list(map(int, lines.pop(0).split()))
            
            while lines and not line.startswith("neh"):
                line = lines.pop(0)

            if not lines:
                break

            data[data_name]["Cmax"] = int(lines.pop(0))
            data[data_name]["NEH"] = []

            while lines and line != "\n":
                line = lines.pop(0)
                data[data_name]["NEH"].extend(
                    list(map(int, line.split()))
                )

    return data

def neh(data):
    n = data["zadania"]
    tasks = data["tasks"]

    # Sort tasks by total processing time in decreasing order
    tasks = sorted(tasks.items(), key=lambda x: sum(x[1]), reverse=True)


    # Initialize time matrix
    time_matrix = Matrix()

    new_task = Task(tasks[0][0], [None] * data['maszyny'])
    for i, gn in enumerate(new_task.maszyny):
        gn.time_to = tasks[0][1][i]
        gn.value = gn.time_to

        if i > 0:
            gn.time_to += new_task.maszyny[i-1].time_to
        
    for i, gn in list(enumerate(new_task.maszyny))[::-1]:
        gn.time_from = tasks[0][1][i]
        if i < len(new_task.maszyny)-1:
            gn.time_from += new_task.maszyny[i+1].time_from
        
    # print(new_task.maszyny)
    time_matrix.matrix = [new_task]

    # print(time_matrix.cmax())

    # Insert remaining tasks
    for i in range(1, n):
        best_time = float('inf')
        best_index = 0
        # print('index', i)
        for j in range(i + 1):
            new_time = time_matrix.get_cmax_after_insert(j, tasks[i])
            # print(new_time, j)
            if new_time < best_time:
                best_time = new_time
                best_index = j

        time_matrix.insert_task(best_index, tasks[i])

    return time_matrix.cmax()

class Task:
    def __init__(self, name, maszyny):
        self.name = name
        self.maszyny = [GraphNode(value) for value in maszyny]

    def __repr__(self):
        return f"Task:{self.name}, m:{self.maszyny}"

class Matrix:
    def __init__(self):
        self.matrix = []

    def cmax(self):
        return self.matrix[0].maszyny[0].time_from

    def get_cmax_after_insert(self,index,task):
        if index > len(self.matrix):
            raise ValueError(f'Index ({index}) grater than matrix size ({len(self.matrix)})')
        cmax = 0
        time_to = 0
        for maszyna, value in enumerate(task[1]):
            time_to = max((self.matrix[index-1].maszyny[maszyna].time_to if index-1>=0 else 0), time_to) + value
            time_from = (self.matrix[index].maszyny[maszyna].time_from if index<=len(self.matrix)-1 else 0)
            new_cmax = time_to + time_from
            # print(time_to - value , value , time_from , '=', new_cmax)
            if new_cmax > cmax:
                cmax = new_cmax
        return cmax
    
    def calculate_time_to(self, index):
        new_time_to = 0
        for maszyna, gn in enumerate(self.matrix[index].maszyny):
            gn.time_to = max((self.matrix[index-1].maszyny[maszyna].time_to if index-1>=0 else 0), new_time_to) + gn.value
            new_time_to = gn.time_to

    def calculate_time_from(self, index):
        new_time_from = 0
        for maszyna, gn in list(enumerate(self.matrix[index].maszyny))[::-1]:
            gn.time_from = gn.value + max((self.matrix[index+1].maszyny[maszyna].time_from if index+1<=len(self.matrix)-1 else 0), new_time_from)
            new_time_from = gn.time_from


    def insert_task(self, index, task):
        # print('insert at',index)
        new_task = Task(task[0], task[1])

        self.matrix.insert(index, new_task)

        self.calculate_time_to(index)
        self.calculate_time_from(index)

        # update time_from
        for i in range(0, index)[::-1]:
            # print('time_from', i)
            self.calculate_time_from(i)

        # update time_to
        for i in range(index+1, len(self.matrix)):
            # print('time_to', i)
            self.calculate_time_to(i)

        # print(self.matrix)


class GraphNode:
    def __init__(self, value=None):
        self.value = value
        self.time_to = 0
        self.time_from = 0

    def __lt__(self, other):
        return self.time_to < other.time

    def __repr__(self):
        return f"({self.value}, to: {self.time_to}, from: {self.time_from})"


def run_neh(instance_data):
    # print("Data:", instance_data)
    # print("NEH:")
    start = time.time()
    cmax = neh(instance_data)
    end = time.time()
    print("Time:", end - start)
    # print(len(schedule) == instance_data["zadania"])
    # print("Schedule:", ' '.join(map(str, schedule)))
    print("Total time:", cmax, instance_data["Cmax"], instance_data["Cmax"] == cmax)
    print()


if __name__ == "__main__":
    data = read_data("neh.data.txt")

    for i, instance_data in data.items():
        print(f"Instance {i}:")
        run_neh(instance_data)
        # break

    # run_neh(data["120"])
            
