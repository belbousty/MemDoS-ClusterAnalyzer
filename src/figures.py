import utils
import matplotlib.pyplot as plt
import os, argparse


def get_stats_load(file: str, stat: str, experiment: str):
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
    labels = ['with running attacks', 'without any attacks']
    markers = ['s', 'o']
    for f, color, label, marker in zip(files,colors,labels, markers):
        stats = utils.extract(stat, f, experiment)
        stats.insert(0,0)
        time = utils.extract('time', f, experiment)
        time.insert(0,0)
        ctime = utils.cumulative_time(time)
        ax.plot(ctime, stats,marker=marker, color=color, label=label)
        ax.fill_between(ctime, stats, color=color,  alpha=0.5)

    if (stat == 'time'):
        plt.title(f"App run time for {file}")
        plt.ylabel("App execution time  (s)")
    elif (stat == 'LLC'):
        plt.title(f"LLC hits for {file}")
        plt.ylabel("LLC hits")
    elif (stat == 'LLC-misses'):
        plt.title(f"LLC misses for {file}")
        plt.ylabel("LLC misses")
    plt.xlabel("Experience time (s)")
    plt.legend()
    plt.savefig(f"figures/{experiment}/{file}-{stat}.png")

def pies(file, experiment):
    '''
    Plot pie figures to show percentages of the LLC hits and misses.
    '''
    plt.figure()
    stats =['LLC','LLC-misses']
    llc = utils.extract(stats[0], file, experiment)
    llc_misses = utils.extract(stats[1], file, experiment)
    llc_m = sum(llc)/len(llc)
    llc_misses_m = sum(llc_misses)/len(llc_misses)
    stats = [llc_m, llc_misses_m]
    colors = ['blue', 'orange']
    explode = (0.1, 0) 
    labels = ['LLC hits', 'LLC misses']
    plt.pie(stats, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(f'LLC stats for {file}')
    plt.savefig(f"figures/{experiment}/{file}.png")




def main(experiment: str):
    '''
    Generate the experiment's figures
    
    Parameters: 
    experiment (str): experiment's filename without the extension

    Returns: 
    None
    '''
    path = f"figures/{experiment}"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    pods = utils.get_pod_names()
    for pod in pods:
        if (utils.check_pod_name(pod, 'victim')):
            utils.save_csv_stats(pod, experiment)
            get_stats_load(pod, 'time', experiment)
            get_stats_load(pod, 'LLC-misses', experiment)
            get_stats_load(pod, 'LLC', experiment)
            pies(pod, experiment)
            pies(pod + '-no-attacks', experiment)

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description=' Launch Experiment.')
    parser.add_argument("--experiment", help="Experiment", default="structure")
    args = parser.parse_args()
    main(args.experiment)