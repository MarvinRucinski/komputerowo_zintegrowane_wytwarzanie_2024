from zad5.data import data


def time(jobs):
    '''
    Returns the completion time of the given data in given order
    jobs is an array of {
        'r': int,
        'p': int,
        'q': int
    }
    '''
    time = 0
    max_q_time = 0
    for job in jobs:
        time = max(time, job['r']) + job['p']
        max_q_time = max(max_q_time, time + job['q'])

    return max_q_time

    

def sort_jobs(jobs):
    # return sorted(jobs, key=lambda x: 5*x['r']-x['p']-5*x['q'])
    jobs = sorted(jobs, key=lambda x: x['r']-x['q'])[::-1]
    sorted_jobs = [jobs[0]]
    jobs = jobs[1:]
    while len(jobs) > 0:
        new_job = jobs.pop(0)
        min_time = time(sorted_jobs + [new_job])
        best_i = 0
        for i in range(len(sorted_jobs) + 1):
            new_time = time(sorted_jobs[:i] + [new_job] + sorted_jobs[i:])
            if new_time < min_time:
                min_time = new_time
                best_i = i
        sorted_jobs.insert(best_i, new_job)

    return sorted_jobs



for i in range(4):
    data[i] = sort_jobs(data[i])
    print(time(data[i]))
    print('---')
    

print(sum(time(data[i]) for i in range(4)))