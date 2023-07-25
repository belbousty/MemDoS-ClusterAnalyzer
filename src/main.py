from kubernetes import client, config
import sys, threading
    
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
        print(f"[-] {dest_node_name} node name doesn't exist")
        sys.exit()
    
    if not is_in_pods(pod_name):
        print(f"[-] {pod_name} doesn't exist in any pod")
        sys.exit()
    
    if pod_in_node(pod_name, dest_node_name):
        print(f"[-] {pod_name} already in node {dest_node_name}")
        sys.exit()   
     
    pod = api_client.read_namespaced_pod(pod_name, pod_namespace)
    pod.metadata.name = new_pod_name
    pod.spec.node_name = dest_node_name
    pod.metadata.uid = None
    pod.metadata.resource_version = None

    delete = threading.Thread(target=deleting_pod, args=(pod_name,pod_namespace))
    create = threading.Thread(target=creating_pod, args=(pod_namespace, pod))
    delete.start()
    create.start()    
    
    while True:
        pod_terminated = is_in_pods(pod_name)
        if pod_terminated : 
            continue
        else: 
            break
    print(f"[+] Migration done")

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




if __name__ == '__main__':
    if (len(sys.argv) != 4 and len(sys.argv) != 5):
        print("[-] Parameters needes : python3 main.py [POD_NAME] [NEW_POD_NAME] [DEST_NODE]")
        sys.exit()
    pod_name = sys.argv[1]
    new_pod_name = sys.argv[2]
    dest_node_name = sys.argv[3]
    if (len(sys.argv) == 5): 
        pod_namespace = sys.argv[4]
    else:
        pod_namespace = 'default'
    migrate_to(pod_name, new_pod_name, dest_node_name, pod_namespace)

