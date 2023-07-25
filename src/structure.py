import yaml
import json

def add_pod_to_config(json_filename):
    file = open(json_filename)
    data = json.load(file)

    with open('config/config.yaml', 'w') as config:
        for pod in data['pods']:
            if (pod['type'] == 'attacker'):
                type = 'attacker'
            else :
                type = 'victim'
            with open(f'config/{type}.yaml', 'r') as attacker:
                yaml_data = yaml.load(attacker, Loader=yaml.FullLoader)
            
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
    