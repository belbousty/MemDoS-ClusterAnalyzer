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
    '''
    Extract nodes and their pods

    Parameters:
    namespace (str): the namespace in which you operate 

    Returns:
    dictionary with the nodes as keys and pods as values 
    '''
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
    '''
    Check status f the pod
    '''
    pod = api_client.read_namespaced_pod(pod_name, pod_namespace)
    return pod.status.conditions[-1].message

def is_in_nodes(node: str):
    '''
    Check if 'node' exists

    Parameters:
    node (str): node's name
    
    Returns:
    bool
    '''
    nodes =  get_nodes()
    if not node in nodes:
        return False
    return True

def is_in_pods(pod: str):
    '''
    Check if 'pod' exists

    Parameters:
    pod (str): pod's name
    
    Returns:
    bool
    '''
    nodes =  get_nodes()
    bool  =  False
    for node in nodes:
        if pod in nodes[node]:
            bool = True                
    return bool

def pod_in_node(pod: str, node: str):
    '''
    Check if 'node' is in 'pod'

    Parameters:
    pod (str): pod's name
    node (str): node's name
    
    Returns:
    bool
    '''
    if not is_in_pods(pod):
        return False
    nodes =  get_nodes()
    if pod in nodes[node]:
        return True
    return False

def deleting_pod(pod_name: str, pod_namespace: str):
    '''
    Delete pod from the apporpriate pod in 'namespace'
    
    Parameters:
    pod_name (str): pod's name
    pod_namespace (str): pod's namespace

    Returns:
    bool
    '''
    try:
        api_client.delete_namespaced_pod(pod_name, pod_namespace)
    except:
        print(f"[-] Error occured while deleting the pod {pod_name}")
        sys.exit()
    print(f"[+] Pod '{pod_name}' terminating")

def creating_pod(pod_namespace: str, pod: str):
    '''
    Create a new pod based on 'pod' properties

    Parameters:
    pod_namespace (str): pod's name
    pod (str): pod's name

    Returns:
    None
    '''
    try :
        api_client.create_namespaced_pod(pod_namespace, pod)
    except: 
        print(f"[-] Error occured while creating the pod {pod.metadata.name}")
        sys.exit()
    print(f"[+] Pod '{pod.metadata.name}' created")


def check_attack_type(attack_type: str):
    '''
    Check if the attack type is correct

    Parameters:
    node (str): attack's type
    
    Returns:
    bool
    '''
    if attack_type in ('lock','llc'):
        return True
    return False

def check_workload(workload: str):
    '''
    Check if the workload set is correct

    Parameters:
    workload (str): workload's name
    
    Returns:
    bool
    '''
    if workload in workloads:
        return True
    return False

def check_benchmark(benchmark: str):
    '''
    Check if the workload set is correct

    Parameters:
    benchmark (str): benchmark's name
    
    Returns:
    bool
    '''
    for workload in workloads:
        if benchmark in workloads[workload]:
            return True 
    return False

def check_pod_name(pod_name: str, role: str):
    '''
    Check the role of the pod (attacker or victim)

    Parameters:
    pod_name (str): the name of the pod
    role (str): role of the pod ('attacker'/'victim')

    Returns:
    bool
    '''
    if (role == 'attacker'):
        pattern = r'attacker.*'
    elif (role == 'victim'):
        pattern = r'victim.*'
    return re.match(pattern, pod_name)

   

def get_experiment_info(info: str, namespace="default"):
    '''
    get a specific information about the experiment

    Parameters:
    info (str): duration, start, attack, apps
    
    Returns:
    dictionary :
        - Duration of the attacks
        - Start time of the attacks
        - type of attacks
        - type of apps for the victims
    '''
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

def exec_command_in_pod(pod_name: str, command: str, namespace='default'):
    '''
    Execute command in a specific pod
    
    Parameters:
    pod_name (str): pod's name
    command (str): command to execute

    Returns:
    response of the command executed
    '''
    try :
        resp = stream(api_client.connect_get_namespaced_pod_exec,
                  pod_name,
                  namespace,
                  command = shlex.split(command),
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
        return resp
    except ValueError as e:
        pass


def get_pod_names(namespace='default'):
    '''
    Get a list of pods' names

    Parameters:
    namespace (str)
    
    Returns:
    list of strings
    '''
    nodes = get_nodes(namespace)
    pods = []
    for node in nodes:
        for pod in nodes[node]:
            pods.append(pod)
    return pods


def extract_performance(output: str):
    '''
    Extract only the perf performance output 

    Parameters:
    output (str): output of the command executed
    
    Returns:
    performance string
    '''
    index = output.find("Performance counter stats for")
    return output[index:]


def perf():
    '''
    the perf command with the appropriate stats

    Parameters:
    None

    Returns:
    perf command (str)
    '''
    return f"./root/perf stat -e LLC,LLC-misses"

def cumulative_time(time):
    '''
    Count cumulative time for a given array

    Parameters:
    time:  array of time

    Returns:
    array
    '''
    cumulative_times = [time[0]]
    for i in range(1, len(time)):
        cumulative_time = 0
        for j in range(0, i+1):
            cumulative_time += float(time[j])
        cumulative_times.append(cumulative_time)
    return cumulative_times