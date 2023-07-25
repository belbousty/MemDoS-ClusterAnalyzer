from kubernetes import client, config
import sys
    
config.load_kube_config()
api_client = client.CoreV1Api()


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