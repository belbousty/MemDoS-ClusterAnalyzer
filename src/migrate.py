import sys, threading, argparse
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






if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=' Launch Experiment.')
    parser.add_argument("--pod", help="Pod name", required=True)
    parser.add_argument("--new-pod", help="New pod name", required=True)
    parser.add_argument("--dest-node", help="Destination Node", required=True)
    parser.add_argument("--namespace", help="Namespace", default='default')
    args = parser.parse_args()

    pod_name = args.pod
    new_pod_name = args.new_pod
    dest_node_name = args.dest_node
    pod_namespace = args.namespace

    
    migrate_to(pod_name, new_pod_name, dest_node_name, pod_namespace)

