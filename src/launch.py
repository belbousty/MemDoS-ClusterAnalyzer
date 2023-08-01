import argparse
import threading, os
import shlex, subprocess, time

import utils



def prepare_victims_benchmarks(pod_name: str):
    '''
    Executes prepare.sh of benchmarks for each victim  
    
    Parameters:
    pod_name (str): the pod's name

    Returns:
    None

    '''

    app = utils.get_experiment_info('app')
    benchmark = app[pod_name]['benchmark']
    workload = app[pod_name]['workload']

    print(f"[+] Starting preparation for {workload} {benchmark} for {pod_name}")
    subprocess.run(shlex.split(f"kubectl exec -it {pod_name} -- '/HiBench/bin/workloads/{workload}/{benchmark}/prepare/prepare.sh'"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] Preparation Ended for {workload} {benchmark}")

def run_victims_apps(duration, pod_name, NoAttack):
    '''
    launch victims apps repeatedly 

    Parameters:
    pod_name (str): the pod's name
    attack (str): attack type (llc or lock)

    Returns:
    None
    '''

    app = utils.get_experiment_info('app')
    benchmark = app[pod_name]['benchmark']
    workload = app[pod_name]['workload']

    print(f"[+] Running {workload} {benchmark} for {pod_name} for {duration} minutes\n")
    filename = pod_name
    if (NoAttack == True):
        filename += "-no-attacks"
     
    with open(f"stats/{filename}.txt", "w") as output_file:
        start_time = time.time()
        while (time.time() - start_time) < (duration * 60):
            res = subprocess.run(shlex.split(f"kubectl exec -it {pod_name} -- {utils.perf()} /HiBench/bin/workloads/{workload}/{benchmark}/hadoop/run.sh"),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output_file.write(utils.extract_performance(res.stdout.decode().strip()))
            output_file.write("\n")
            output_file.write("----------------\n")
    print(f"[+] Application ended for {pod_name}\n")
    

    
def launch_attacks(pod_name, attack):
    '''
    launch attackers in attackers pods

    Parameters:
    pod_name (str): the pod's name
    attack (str): attack type (llc or lock)

    Returns:
    None
    '''
    if (attack == 'llc'):
        binary = 'llcCleansing'
    else:
        binary = 'atomicLocking'

    start = utils.get_experiment_info('start')
    
    pod_start = int(start[pod_name])*60

    duration = utils.get_experiment_info('duration')
    pod_duration = int(duration[pod_name])*60

    print(f"[+] Starting {pod_name} attack\n")
    subprocess.run(shlex.split(
                f'kubectl exec -it {pod_name} -- /bin/sh -c "sleep {pod_start} && timeout {pod_duration} /root/{binary}"'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] {pod_name} attack ended\n")


def launch_experiment(duration: int, NoAttacks: bool, namespace='default'):
    '''
    launch Experiment

    Parameters:
    duration (int): total duration of the experiment

    Returns:
    None
    '''

    pods = utils.get_pod_names(namespace)

    threads = []
    for pod_name in pods:
        if (utils.check_pod_name(pod_name, 'victim')):
            prepare_victims_benchmarks(pod_name)
            thread = threading.Thread(
                target = run_victims_apps,
                args = (duration,
                        pod_name, NoAttacks))
            threads.append(thread)
        if (utils.check_pod_name(pod_name, 'attacker') and NoAttacks == False):
            thread = threading.Thread(
                target=launch_attacks,
                args=(pod_name,
                      utils.get_experiment_info('attack')
                    )
            )
            threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=' Launch Experiment.')
    parser.add_argument("--duration", type=int, help="Expirement duration in minutes", default= 10, required=True)
    parser.add_argument("--no-attacks", action="store_true", help="No attack will be launched")

    path = "stats"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    args = parser.parse_args()
    launch_experiment(args.duration, args.no_attacks)
