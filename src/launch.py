import argparse
import threading, os
import utils

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
            utils.prepare_victims_benchmarks(pod_name)
            thread = threading.Thread(
                target = utils.run_victims_apps,
                args = (duration,
                        pod_name, NoAttacks))
            threads.append(thread)

        if (utils.check_pod_name(pod_name, 'attacker') and NoAttacks == False):
            thread = threading.Thread(
                target=utils.launch_attacks,
                args=(pod_name,)
            )
            threads.append(thread)

    print("[+] Starting experiment")
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("[+] Experiment Ended")
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=' Launch Experiment.')
    parser.add_argument("--duration", type=int, help="Expirement duration in minutes", required=True)
    parser.add_argument("--no-attacks", action="store_true", help="No attack will be launched")

    path = "stats"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    args = parser.parse_args()
    launch_experiment(args.duration, args.no_attacks)
