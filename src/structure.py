import yaml
import json
import utils
import sys
import argparse

def num_node(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    num = 1
    for info in data:
        for pod in data[info]:
            if (int(pod['node']) > num):
                num = int(pod['node'])
    return num


def get_pod_name(cursor, role, node):
    return role + node + f'{cursor[node][role]}'
    

def get_node_name(node_number):
    node_name = "minikube"
    if (node_number == '1'):
        return node_name
    return node_name + f"-m0{node_number}"

def change_values(yaml_data ,pod, role, cursor):
    yaml_data['spec']['nodeName'] = get_node_name(pod['node'])
    yaml_data['metadata']['name'] = get_pod_name(cursor, role, pod['node'])

def get_full_json(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    
    cursor = {}
    for i in range(num_node(file)):
        cursor[str(i + 1)] = {'attacker': 1, 'victim' : 1}

    with open('config/config.yaml', 'w') as config:
        for attacker in data['attackers']:
            with open(f'config/attacker.yaml', 'r') as att:
                yaml_data = yaml.load(att, Loader=yaml.FullLoader) 
           
            if not utils.check_attack_type(attacker['attackType']):
                print(f"[-]{attacker['attackType']} is not an attack")
                sys.exit()
            yaml_data['metadata']['annotations']['attackType'] = attacker['attackType']
            yaml_data['metadata']['annotations']['duration'] = attacker['duration']
            yaml_data['metadata']['annotations']['start'] = attacker['start']
            change_values(yaml_data, attacker, 'attacker', cursor)
            cursor[attacker['node']]['attacker'] += 1
            yaml.dump(yaml_data, config, sort_keys=False, default_flow_style=None) 
            config.write('\n---\n')

        
        for victim in data['victims']:
            with open(f'config/victim.yaml', 'r') as vict:
                yaml_data = yaml.load(vict, Loader=yaml.FullLoader)
            
            if not utils.check_workload(victim['workload']):
                print(f"[-] {victim['workload']} is not a workload")
                print(f"    You have to choose a workload from this list:")
                for workload in utils.workloads:
                    print(f"    - {workload}")
                sys.exit()
            yaml_data['metadata']['annotations']['workload'] = victim['workload']
            
            if not utils.check_benchmark(victim['benchmark']):
                print(f"[-] {victim['benchmark']} is not a benchmark")
                print(f"    You have to choose a benchmark from this list:")
                for benchmark in utils.workloads[victim['workload']]:
                    print(f"    - {benchmark}")
                sys.exit()
            yaml_data['metadata']['annotations']['benchmark'] = victim['benchmark']
            change_values(yaml_data, victim, 'victim', cursor)
            cursor[victim['node']]['victim'] += 1
            yaml.dump(yaml_data, config, sort_keys=False, default_flow_style=None) 
            config.write('\n---\n')    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="json file path", default= 'structure.json')
    args = parser.parse_args()

    get_full_json(args.json)