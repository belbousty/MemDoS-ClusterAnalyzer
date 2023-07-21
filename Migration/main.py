from kubernetes import client, config
from prometheus_client import start_http_server, Summary, Gauge
from prometheus_client.parser import text_string_to_metric_families
import subprocess
import requests
import time
    
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

def migrate_to(pod_name, new_pod_name, dest_node_name, pod_namespace = "default"):

    if not is_in_nodes(dest_node_name):
        print(f"{dest_node_name} node name doesn't exist")
        return None
    
    if pod_in_node(pod_name, dest_node_name):
        print(f"{pod_name} already in node {dest_node_name}")
        return None    

    pod = api_client.read_namespaced_pod(pod_name, pod_namespace)
    pod.metadata.name = new_pod_name
    pod.spec.node_name = dest_node_name
    pod.metadata.uid = None
    pod.metadata.resource_version = None
    try:
        api_client.delete_namespaced_pod(pod_name, pod_namespace)
    except:
        print(f"Error occured while deleting the pod")
        
    while True:
        pod_terminated = is_in_pods(pod_name)
        if pod_terminated : 
            continue
        else: 
            break
    try :
        api_client.create_namespaced_pod(pod_namespace, pod)
    except: print(f"Error occured whil  creating the pod")

if __name__ == '__main__':
    migrate_to('pod-11', 'pod-03', 'minikube')

