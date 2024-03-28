import time
import multiprocessing 

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

def check_schedule(data, task, schedule, j):
    new_schedule = schedule[:j] + [task[0]] + schedule[j:]
    new_time = calculate_schedule_time(data, new_schedule)
    return new_time, j

def neh(data):
    n = data["zadania"]
    tasks = data["tasks"]

    # Sort tasks by total processing time in decreasing order
    tasks = sorted(tasks.items(), key=lambda x: sum(x[1]), reverse=True)

    # Initialize schedule with first two tasks
    schedule = [tasks[0][0]]
    best_time_overall = calculate_schedule_time(data, schedule)

    # Insert remaining tasks
    for i in range(1, n):
        best_time = float('inf')
        best_index = 0

        with multiprocessing.Pool() as pool:
            results = [pool.apply_async(check_schedule, (data, tasks[i], schedule, j)) for j in range(i + 1)]
            results = [r.get() for r in results]
            for new_time, j in results:
                if new_time < best_time:
                    best_time = new_time
                    best_index = j

        schedule.insert(best_index, tasks[i][0])
        best_time_overall = best_time

    return schedule, best_time_overall


def calculate_schedule_time(data, schedule):
    n = data["zadania"]
    m = data["maszyny"]
    tasks = data["tasks"]

    # Initialize time matrix
    time_matrix = [[0 for _ in range(m)] for _ in range(n)]

    cmax = 0

    # Calculate time matrix
    for i, task in enumerate(schedule):
        for j in range(m):
            if i == 0:
                time_matrix[i][j] = (tasks[task][j] + time_matrix[i][j-1]) if j > 0 else tasks[task][j]
            else:
                time_matrix[i][j] = max(time_matrix[i-1][j], time_matrix[i][j-1]) + tasks[task][j]
        cmax = max(cmax, time_matrix[i][m-1])

    
    return cmax



def run_neh(instance_data):
    # print("Data:", instance_data)
    # print("NEH:")
    start = time.time()
    schedule, cmax = neh(instance_data)
    end = time.time()
    print("Time:", end - start)
    # print(len(schedule) == instance_data["zadania"])
    # print("Schedule:", ' '.join(map(str, schedule)))
    print("Total time:", cmax, instance_data["Cmax"], instance_data["Cmax"] >= cmax)
    print()


if __name__ == "__main__":
    data = read_data("neh.data.txt")

    # for i, instance_data in data.items():
    #     print(f"Instance {i}:")
    #     run_neh(instance_data)

    run_neh(data["120"])
            
