import sys, threading, argparse
import json, time
import csv
import utils

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
    
    while True:
        pod_terminated = utils.is_in_pods(pod_name)
        if pod_terminated :
            continue
        else: 
            break
    print(f"[+] Migration done")


def get_metrics_without_attack(namespace = 'default'):
    pods = utils.get_pod_names(namespace)
    pods_metrics = {}
    for pod in pods:
        if (utils.check_pod_name(pod, 'victim')):
            pods_metrics[pod] = []
            with open(f"stats/csv/{pod}-no-attacks.csv") as file:
                csvreader = csv.reader(file)
                next(csvreader)
                for row in csvreader:
                    avr = sum(json.loads(row[1]))/len(json.loads(row[1]))
                    pods_metrics[pod].append({row[0]: f'{avr}'})
    return pods_metrics


def check_app_execution_time(pod):    
    actual_time = 0
    average_time = float(get_metrics_without_attack()[pod][0]['time'])
    with open(f"stats/csv/{pod}.csv") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            if (row[0] == 'time'):
                actual_time = json.loads(row[1])[0]
    if actual_time > average_time:
        return True
    return False

def check_app_llc_misses(pod, average_llc_misses):
    average_llc_misses = float(get_metrics_without_attack()[pod][0]['LLC-misses'])
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

def check_co_residence_time(pod, namespace='default'):
    pods = utils.get_pod_names(namespace)
    # #######
    pass

def victim_thread(pod):
    while (1):
        utils.prepare_victims_benchmarks(pod)
        utils.run_victims_apps('Don`t matter', pod, False)
        if (check_app_execution_time(pod)):
            # Migrate
            return True
        if (check_app_llc_misses(pod)):
            # Migrate
            return True

if __name__ == '__main__':
    print(get_metrics_without_attack())

