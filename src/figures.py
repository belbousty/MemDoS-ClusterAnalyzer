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

# def get_stats_load(file):
#     #stats =['LLC-load-misses', 'LLC-loads', 'LLC-store-misses', 'LLC-stores', 'cache-misses', 'cache-references']
#     time = extract("time", file)
#     ctime = cumulative_time(time)
#     load_misses = extract('LLC-load-misses', file)
#     loads = extract('LLC-loads', file)

#     plt.plot(ctime, load_misses, marker='o', linestyle='-', color='r')
#     plt.plot(ctime, loads, marker='o', linestyle='-', color='g')
    
#     plt.xlabel('time')
    
#     plt.show()

def get_stats_load(file):
    stats =['LLC','LLC-misses', 'time']
    total = extract(stats[0], file)
    LLC = [total[0]]
    for  i in range(2,len(total),2):
        LLC.append(total[i])
    
    for i in range(0,len(LLC)):
        plt.bar(i, LLC[i], linestyle='-', color='b')
    
    misses = extract(stats[1], file)
    for i in range(0,len(misses)):    
        plt.bar(i, misses[i], linestyle='-', color='red')
    plt.xticks([], [])
    plt.title(f"LLC stats ({file})")
    plt.show()

    time = extract(stats[2], file)
    for i in range(0,len(time)):    
        plt.bar(i, time[i], linestyle='-', color='green')

    plt.title(f"App run time {file}")
    plt.ylabel("time in seconds")
    plt.show()

if __name__ == '__main__' :
    get_stats_load('victim00')
    get_stats_load('victim10')
    pass