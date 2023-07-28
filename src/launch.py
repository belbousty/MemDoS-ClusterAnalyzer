import argparse
import utils
import threading, sys
from kubernetes.client.exceptions import ApiException
import shlex
import subprocess
import time

lock = threading.Lock()

def prepare_victims_benchmarks(pod_name):
    app = utils.get_experiment_info('app')
    benchmark = app[pod_name]['benchmark']
    workload = app[pod_name]['workload']

    print(f"    [+] Starting preparation for {workload} {benchmark} for {pod_name}")
    subprocess.run(shlex.split(f"kubectl exec -it {pod_name} -- '/HiBench/bin/workloads/{workload}/{benchmark}/prepare/prepare.sh'"))
    print(f"    [+] Preparation Ended for {workload} {benchmark}")

def run_victims_apps(duration, pod_name):
    app = utils.get_experiment_info('app')
    benchmark = app[pod_name]['benchmark']
    workload = app[pod_name]['workload']

    print(f"    [+] Running {workload} {benchmark} for {pod_name} for {duration} minutes")
    start_time = time.time()
    while (time.time() - start_time) < (duration * 60):
        subprocess.run(shlex.split(f"kubectl exec -it {pod_name} -- '/HiBench/bin/workloads/{workload}/{benchmark}/hadoop/run.sh' &"), stdout=subprocess.DEVNULL)
    print(f"    [+] Application ended for {pod_name}")
    
def launch_attacks(pod_name, attack):
    if (attack == 'llc'):
        binary = 'llcCleansing'
    else:
        binary = 'atomicLocking'

    start = utils.get_experiment_info('start')
    
    pod_start = int(start[pod_name])*60

    duration = utils.get_experiment_info('duration')
    pod_duration = int(duration[pod_name])*60

    print(f"[+] Starting {pod_name} attack")
    subprocess.run(shlex.split(
                f'kubectl exec -it {pod_name} -- timeout {pod_duration} /root/{binary}'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] {pod_name} attack ended")

##
# duration sould be at least bigger than the biggest attack duration
##
def launch_experiment(duration, namespace='default'):

    pods = utils.get_pod_names(namespace)

    threads = []
    for pod_name in pods:
        # if (utils.check_pod_name(pod_name, 'victim')):
        #     #prepare_victims_benchmarks(pod_name)
        #     thread = threading.Thread(
        #         target = run_victims_apps,
        #         args = (duration,
        #                 pod_name))
        #     threads.append(thread)
        if (utils.check_pod_name(pod_name, 'attacker')):
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

    args = parser.parse_args()
    launch_experiment(args.duration)
    print(shlex.split(
                f'kubectl exec -it attakcer -- "sleep aaaa && timeoout 2 ./root/aa" &'))