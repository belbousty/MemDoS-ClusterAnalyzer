import utils
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
    elif stat == 'LLC':
        pattern = r"^\s+(\d+)\s+LLC\s*$" 
    elif stat == 'LLC-misses':
        pattern = r"(\d+)\s+LLC-misses"
    stats = []
    for line in lines:
        matches = re.findall(pattern, line)
        if (len(matches)):
            stats.append(float(matches[0]))
    return stats


def get_stats_load(file: str, stat):
    '''
    Plot statistics for a specific victim
    
    Parameters:
    file (str): name of the victim 

    Returns:
    None
    
    '''
    stats =['LLC','LLC-misses']
    fig, ax = plt.subplots()
    files = [file, file+"-no-attacks"]
    colors = ['red', 'green']
    labels = ['with runing attacks', 'without any attacks']
    markers = ['s', 'o']
    ymax = 0
    for f, color, label, marker in zip(files,colors,labels, markers):
        stats = extract(stat, f)
        stats.insert(0,0)
        time = extract('time', f)
        time.insert(0,0)
        ctime = cumulative_time(time)
        ax.plot(ctime, stats,marker=marker, color=color, label=label)
        ax.fill_between(ctime, stats, color=color,  alpha=0.5)
        if (max(stats) > ymax):
            ymax = max(stats)
    # ax.vlines(x = 0,ymin=0, ymax=ymax, color = 'b')
    # ax.vlines(x = 300, ymin=0, ymax=ymax, color = 'b')

    # ax.fill_betweenx(y=[0, ymax], x1=60, x2=240, color='lightblue', alpha=0.3, label='Attack Period')
    if (stat == 'time'):
        plt.title(f"App run time for {file}")
        plt.ylabel("App Execution time  (s)")
    elif (stat == 'LLC'):
        plt.title(f"LLC hits for {file}")
        plt.ylabel("LLC hits")
    elif (stat == 'LLC-misses'):
        plt.title(f"LLC misses for {file}")
        plt.ylabel("LLC misses")
    plt.xlabel("Experience time (s)")
    plt.legend()
    plt.show()

def pies(file):
    stats =['LLC','LLC-misses']
    llc = extract(stats[0], file)
    llc_misses = extract(stats[1], file)
    llc_m = sum(llc)/len(llc)
    llc_misses_m = sum(llc_misses)/len(llc_misses)
    stats = [llc_m, llc_misses_m]
    colors = ['blue', 'orange']
    explode = (0.1, 0) 
    labels = ['LLC hist', 'LLC misses']
    plt.pie(stats, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(f'LLC stats for {file}')
    plt.show()


def main():
    pods = utils.get_pod_names()
    for pod in pods:
        if (utils.check_pod_name(pod, 'victim')):
            get_stats_load(pod, 'time')
            get_stats_load(pod, 'LLC-misses')
            get_stats_load(pod, 'LLC')
            pies(pod)
            pies(pod+'-no-attacks')

if __name__ == '__main__' :
    main()
    pass