from kubernetes import client, config
from kubernetes.stream import stream
import sys, re
import shlex

config.load_kube_config()
api_client = client.CoreV1Api()

workloads = {
    'graph': ['nweight', 'pagerank'], 
    'micro': ['dfsioe', 'repartition', 'sleep', 'sort', 'terasort', 'wordcount'], 
    'ml': ['als', 'bayes', 'correlation', 'gbt', 'gmm', 'kmeans', 'lda', 'linear', 'lr', 'pca', 'rf', 'summarizer', 'svd', 'svm', 'xgboost'],
    'sql': ['aggregation', 'common', 'join', 'scan'],
    'streaming': ['fixwindow', 'identity', 'repartition', 'wordcount'], 
    'websearch' : ['nutchindexing', 'pagerank']
    }

def get_nodes(namespace = "default"):
    Nodes = api_client.list_node().items
    nodes = {}
    for node in Nodes:
        node_name = node.metadata.name
        nodes[node_name] = []
        pods = api_client.list_namespaced_pod(namespace, field_selector = f"spec.nodeName={node_name}").items
        for pod in pods:
            nodes[node_name].append(pod.metadata.name)
    return nodes


def get_pod_status(pod_name, pod_namespace = "default"):
    pod = api_client.read_namespaced_pod(pod_name, pod_namespace)
    return pod.status.conditions[-1].message

def is_in_nodes(node):
    nodes =  get_nodes()
    if not node in nodes:
        return False
    return True

def is_in_pods(pod):
    nodes =  get_nodes()
    bool  =  False
    for node in nodes:
        if pod in nodes[node]:
            bool = True                
    return bool

def pod_in_node(pod, node):
    if not is_in_pods(pod):
        return False
    nodes =  get_nodes()
    if pod in nodes[node]:
        return True
    return False

def deleting_pod(pod_name, pod_namespace):
    try:
        api_client.delete_namespaced_pod(pod_name, pod_namespace)
    except:
        print(f"[-] Error occured while deleting the pod {pod_name}")
        sys.exit()
    print(f"[+] Pod '{pod_name}' terminating")

def creating_pod(pod_namespace, pod):
    try :
        api_client.create_namespaced_pod(pod_namespace, pod)
    except: 
        print(f"[-] Error occured while creating the pod {pod.metadata.name}")
        sys.exit()
    print(f"[+] Pod '{pod.metadata.name}' created")


def check_attack_type(attack_type):
    if attack_type in ('lock','llc'):
        return True
    return False

def check_workload(workload):
    if workload in workloads:
        return True
    return False

def check_benchmark(benchmark):
    for workload in workloads:
        if benchmark in workloads[workload]:
            return True 
    return False

def check_pod_name(pod_name, role):
    if (role == 'attacker'):
        pattern = r'attacker.*'
    elif (role == 'victim'):
        pattern = r'victim.*'
    return re.match(pattern, pod_name)

   
##
#  info could be: 'duration', 'start', 'app', 'attack
##
def get_experiment_info(info, namespace="default"):
    pods = api_client.list_namespaced_pod(namespace).items
    nodes = get_nodes(namespace)
    infos = {}
    for pod in pods:
        nodeName = pod.spec.node_name
        if (info in ('duration', 'start', 'attack')):
            if (check_pod_name(pod.metadata.name, 'attacker') and nodeName in nodes):
                if info == 'attack':
                    infos[pod.metadata.name] = pod.metadata.annotations['attackType']
                else:
                    infos[pod.metadata.name] =  pod.metadata.annotations[info]
        elif (info == 'app'):
            if (check_pod_name(pod.metadata.name, 'victim') and nodeName in nodes):
        
                infos[pod.metadata.name] = {
                    'benchmark' :pod.metadata.annotations['benchmark'],
                    'workload' : pod.metadata.annotations['workload']
                }
    return infos

def exec_command_in_pod(pod_name, command, namespace='default'):
    resp = stream(api_client.connect_get_namespaced_pod_exec,
                  pod_name,
                  namespace,
                  command = shlex.split(command),
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    return resp

def get_pod_names(namespace='default'):
    nodes = get_nodes(namespace)
    pods = []
    for node in nodes:
        for pod in nodes[node]:
            pods.append(pod)
    return pods

