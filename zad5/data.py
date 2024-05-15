
def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    data = {}
    while lines:
        line = lines.pop(0)
        if line.startswith("data."):
            data_name = line.split('data.')[1].strip(':\n')
            data[data_name] = {}
            i = int(lines.pop(0))
            data[data_name]["zadania"] = i
            data[data_name]["tasks"] = {}
            for i in range(i):
                data[data_name]["tasks"][i] = list(map(int, lines.pop(0).split()))
            
            while lines and not line.startswith("carl"):
                line = lines.pop(0)

            if not lines:
                break

            data[data_name]["Cmax"] = int(lines.pop(0))
            data[data_name]["carl"] = []

            while lines and line != "\n":
                line = lines.pop(0)
                data[data_name]["carl"].extend(
                    list(map(int, line.split()))
                )
    return data

data = read_data("carl.data.txt")