import sys, threading
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

