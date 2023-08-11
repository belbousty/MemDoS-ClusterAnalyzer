import sys, threading, argparse
import json, time
import csv
import utils

prepared_pods = []
deleting_pods = []
nodes_score = {}

pods = utils.get_pod_names()
for pod in pods:
    if (utils.check_pod_name(pod, 'victim')):
        prepared_pods.append(pod)


def migrate_to(pod_name, new_pod_name, dest_node_name, pod_namespace = "default"):

    if not utils.is_in_nodes(dest_node_name):
        print(f"[-] {dest_node_name} node name doesn't exist")
        sys.exit()
    
    if not utils.is_in_pods(pod_name):
        print(f"[-] {pod_name} doesn't exist in any pod")
        sys.exit()
    
    if utils.pod_in_node(pod_name, dest_node_name):
        print(f"[-] {pod_name} already in node {dest_node_name}")
        sys.exit()   
     
    pod = utils.api_client.read_namespaced_pod(pod_name, pod_namespace)
    pod.metadata.name = new_pod_name
    pod.spec.node_name = dest_node_name
    pod.metadata.uid = None
    pod.metadata.resource_version = None

    delete = threading.Thread(target=utils.deleting_pod, args=(pod_name,pod_namespace))
    create = threading.Thread(target=utils.creating_pod, args=(pod_namespace, pod))
    delete.start()
    create.start()    
    
    deleting_pods.append(pod_name)
    while True:
        pod_terminated = utils.is_in_pods(pod_name)
        if pod_terminated :
            continue
        else: 
            break
    deleting_pods.remove(pod_name)
    print(f"[+] Migration done")

def evaluate_nodes_score(namespace='default'):
    nodes = utils.get_nodes(namespace)
    # First Criteria : Number of pods
    for node in nodes:
        nodes_score[node] = len(nodes[node])
    

def choose_destination(pod, namespace='default'):
    nodes = utils.get_nodes(namespace)
    pod_node = False
    for node in nodes:
        if (utils.pod_in_node(pod, node)):
            pod_node = node
            break
    if pod_node == False:
        print("pod doesnt exist")
        exit()
    nodes_score_copy = nodes_score.copy()
    del nodes_score_copy[pod_node]

    minimum = min(nodes_score_copy.values())
    min_node = False
    for  node, value in nodes_score_copy.items():
        if minimum == value:
            min_node = node
    return min_node

def get_metrics_without_attack(namespace = 'default'):

    pods = utils.get_pod_names(namespace)
    pods_metrics = {}
    for pod in pods:
        if (utils.check_pod_name(pod, 'victim')):
            pods_metrics[pod] = []
            utils.save_csv_stats(pod)
            with open(f"stats/csv/{pod}-no-attacks.csv") as file:
                csvreader = csv.reader(file)
                next(csvreader)
                for row in csvreader:
                    avr = sum(json.loads(row[1]))/len(json.loads(row[1]))
                    pods_metrics[pod].append({row[0]: f'{avr}'})
    return pods_metrics


def check_app_execution_time(pod):    
    actual_time = 0
    average_time = float(get_metrics_without_attack()[pod][2]['time'])
    with open(f"stats/csv/{pod}.csv") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            if (row[0] == 'time'):
                actual_time = json.loads(row[1])[0]
    if actual_time > average_time:
        return True
    return False

def check_app_llc_misses(pod):
    average_llc_misses = float(get_metrics_without_attack()[pod][1]['LLC-misses'])
    file = f'stats/csv/{pod}.csv'
    with open(file) as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            if (row[0] == 'LLC-misses'):
                actual_llc_misses = json.loads(row[1])[0]
            else : 
                actual_llc_misses = 0
    if (actual_llc_misses > average_llc_misses):
        return True
    return False


def victim_thread(duration, pod, namespace='default'):
    utils.prepare_victims_benchmarks(pod)
    start_time = time.time()
    while (time.time() - start_time) < (duration * 60):
        utils.run_victims_apps(duration, pod, False, 'Migration')
        if (check_app_execution_time(pod)):

            migrate_to(pod, pod+"-m",choose_destination(pod, namespace), namespace)
            prepared_pods.remove(pod)
            print('Migrate due to execution time!')
            return True
        if (check_app_llc_misses(pod)):
            prepared_pods.remove(pod)
            print('Migrate due to llc misses!')
            return True

def attacker_thread(pod, namespace='default'):
    utils.launch_attacks(pod)


def NewPods_prep_thread(namespace='default'):
    pods = utils.get_pod_names(namespace)
    for pod in pods:
        if (utils.check_pod_name(pod, 'victim')):
            if (not pod in prepared_pods) and (not pod in deleting_pods):
                utils.prepare_victims_benchmarks(pod)
                prepared_pods.append(pod)


def launch_without_attack(duration: int, namespace='default'):
    pods = utils.get_pod_names(namespace)
    pod_threads = []
    for pod_name in pods:
        
        if (utils.check_pod_name(pod_name, 'victim')):
            thread = threading.Thread(
                target = utils.run_victims_apps,
                args = (duration,
                        pod_name,
                        True))
            pod_threads.append(thread)
    for thread in pod_threads:
        thread.start()
    for thread in pod_threads:
        thread.join()
        
def launch(duration: int, namespace='default'):
    # print("[+] Starting experiment without attack")
    # launch_without_attack(duration, namespace)
    # print("[+] No attacks experiment ended! ")

    pods = utils.get_pod_names(namespace)
    pod_threads = []
    for pod_name in pods:
        
        if (utils.check_pod_name(pod_name, 'victim')):
            thread = threading.Thread(
                target = victim_thread,
                args = (duration,
                        pod_name))
            pod_threads.append(thread)
        if (utils.check_pod_name(pod_name, 'attacker')):
            thread = threading.Thread(
                target=utils.launch_attacks,
                args=(pod_name,)
            )
            pod_threads.append(thread)

    thread = threading.Thread(
        target=NewPods_prep_thread,
        args=(namespace,)
    )
    pod_threads.append(thread)

    thread = threading.Thread(
        target=evaluate_nodes_score,
        args=(namespace,)
    )
    pod_threads.append(thread)
    print("[+] Starting experiment")
    for thread in pod_threads:
        thread.start()
    for thread in pod_threads:
        thread.join()
    print("[+] Experiment ended! ")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' Launch Experiment with a migration strategy.')
    parser.add_argument("--duration", type=int, help="Expirement duration in minutes", required=True)

    args = parser.parse_args()
    launch(args.duration)

