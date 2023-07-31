import matplotlib.pyplot as plt
import re 


def cumulative_time(time):
    cumulative_times = [time[0]]
    for i in range(1, len(time)):
        cumulative_time = 0
        for j in range(0, i+1):
            cumulative_time += float(time[j])
        cumulative_times.append(cumulative_time)
    return cumulative_times

def extract(stat, victim):
    with open(f"stats/{victim}.txt", "r") as f:
        lines = f.readlines()
    if (stat == 'time'):
        pattern = r"(\d+\.\d+) seconds time elapsed"
    else:
        pattern = f"(\d+)\s+{stat}" 
    stats = []
    for line in lines:
        matches = re.findall(pattern, line)
        if (len(matches)):
            stats.append(float(matches[0]))
    return stats

def get_stats(file):
    stats =['LLC-load-misses', 'LLC-loads', 'LLC-store-misses', 'LLC-stores', 'cache-misses', 'cache-references']
    time = extract("time", file)
    ctime = cumulative_time(time)
    for i in range(0, len(stats)):
        stat = extract(stats[i], file)
        plt.plot(ctime, stat, marker='o', linestyle='-', color='b')
        plt.xlabel('time')
        plt.ylabel(f'{stats[i]}')
        plt.show()

if __name__ == '__main__' :
    get_stats('victim10')
    pass