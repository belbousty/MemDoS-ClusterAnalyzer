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

def extract(stat :str, victim: str):
    '''
    Extract values of statistic properties

    Parameters:
    stat (str): either 'time', 'LLC', 'LLC-misses'
    victim (str): name of the victim pod (victimXX)

    Returns:
    statistic property values during the experience
    '''
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


def get_stats_load(file: str):
    '''
    Plot statistics for a specific victim
    
    Parameters:
    file (str): name of the victim 

    Returns:
    None
    
    '''
    stats =['LLC','LLC-misses', 'time']
    # total = extract(stats[0], file)
    # LLC = [total[0]]
    # for  i in range(2,len(total),2):
    #     LLC.append(total[i])
    
    # for i in range(0,len(LLC)):
    #     plt.bar(i, LLC[i], linestyle='-', color='b')
    
    # misses = extract(stats[1], file)
    # for i in range(0,len(misses)):    
    #     plt.bar(i, misses[i], linestyle='-', color='red')
    # plt.xticks([], [])
    # plt.title(f"LLC stats ({file})")
    # plt.show()

    # plot execution time of the app during experience
    fig, ax = plt.subplots()
    files = [file, file+"-no-attacks"]
    colors = ['red', 'green']
    labels = ['with runing attacks', 'without any attacks']
    for file, color, label in zip(files,colors,labels):
        time = extract(stats[2], file)
        time.insert(0,0)
        ctime = cumulative_time(time)
        ax.plot(ctime, time,marker='o', color=color, label=label)
        ax.fill_between(ctime, time, color=color,  alpha=0.5)

    #plt.title(f"App run time {file}")
    plt.ylabel("App Execution time  (s)")
    plt.xlabel("Experience time (s)")
    plt.title("App Run Time")
    plt.legend()
    plt.show()






if __name__ == '__main__' :
    get_stats_load('victim00')
    #get_stats_load('victim10')
    pass