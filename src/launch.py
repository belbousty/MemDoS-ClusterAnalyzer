import argparse
import utils
import threading
import shlex

def launch_victims_apps(pod_name):
    app = utils.get_experiment_info('app')
    benchmark = app[pod_name]['benchmark']
    workload = app[pod_name]['workload']

    print(f"    [+] Starting preparation for {workload} {benchmark} for {pod_name}")
    utils.exec_command_in_pod(pod_name,
                f"/HiBench/bin/workloads/{workload}/{benchmark}/prepare/prepare.sh")
    print(f"    [+] Preparation Ended for {workload} {benchmark}")
    
    print(f"    [+] Running {workload} {benchmark} for {pod_name}")
    utils.exec_command_in_pod(pod_name,
                f"/HiBench/bin/workloads/{workload}/{benchmark}/hadoop/run.sh")
    print(f"    [+] Application ended for {pod_name}")
    pass

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
    utils.exec_command_in_pod(pod_name,
                f'/bin/sh -c "sleep {pod_start} && timeout {pod_duration} ./root/{binary}"')
    print(f"[+] {pod_name} attack ended")

##
# duration sould be at least bigger than the biggest attack duration
##
def launch_experiment(duration, namespace='default'):
    pods = utils.get_pod_names(namespace)
    for pod_name in pods:
        # Launch apps first
        if (utils.check_pod_name(pod_name, 'victim')):
            print(f'[+] Starting app for {pod_name}')
            launch_victims_apps(pod_name)
    attack_threads = []
    for pod_name in pods:
        if (utils.check_pod_name(pod_name, 'attacker')):
            thread = threading.Thread(
                target=launch_attacks,
                args=(pod_name,
                      utils.get_experiment_info('attack')
                    )
            )
            attack_threads.append(thread)
    for thread in attack_threads:
        thread.start()
    for thread in attack_threads:
        thread.join()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=' Launch Experiment.')
    parser.add_argument("--duration", type=int, help="Expirement duration in minutes", default= 10, required=True)

    args = parser.parse_args()
    launch_experiment(args.duration)
    pass