import yaml
import json
import utils
import sys


def add_pod_to_config(json_filename):

    with open(json_filename, 'r') as file:
        data = json.load(file)

    with open('config/config.yaml', 'w') as config:
        for pod in data['pods']:
            if (pod['type'] == 'attacker'):
                type = 'attacker'
            else :
                type = 'victim'
            with open(f'config/{type}.yaml', 'r') as attacker:
                yaml_data = yaml.load(attacker, Loader=yaml.FullLoader)
            
            if type == 'attacker':
                if not utils.check_attack_type(pod['attackType']):
                    print(f"[-]{pod['attackType']} is not a workload")
                    sys.exit()
                yaml_data['metadata']['annotations']['attackType'] = pod['attackType']
                yaml_data['metadata']['annotations']['duration'] = pod['duration']
                yaml_data['metadata']['annotations']['start'] = pod['start']
            else:
                if not utils.check_workload(pod['workload']):
                    print(f"[-] {pod['workload']} is not a workload")
                    sys.exit()
                yaml_data['metadata']['annotations']['workload'] = pod['workload']
                
                if not utils.check_benchmark(pod['benchmark']):
                    print(f"[-] {pod['benchmark']} is not a benchmark")
                    sys.exit()
                yaml_data['metadata']['annotations']['benchmark'] = pod['benchmark']
                
            yaml_data['spec']['nodeName'] = pod['nodeName']
            yaml_data['metadata']['name'] = pod['name']
            
            yaml_data['spec']['containers'][0]['image'] = pod['image']
            yaml_data['spec']['containers'][0]['resources']['limits']['memory'] = pod['limits'][0]['memory']
            yaml_data['spec']['containers'][0]['resources']['limits']['cpu'] = pod['limits'][0]['cpu']
            yaml_data['spec']['containers'][0]['resources']['requests']['memory'] = pod['requests'][0]['memory']
            yaml_data['spec']['containers'][0]['resources']['requests']['cpu'] = pod['requests'][0]['cpu']

            yaml.dump(yaml_data, config, sort_keys=False, default_flow_style=None) 
            
            config.write('\n---\n')

if __name__ == '__main__':
    add_pod_to_config('structure.json')
    