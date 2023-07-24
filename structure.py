import yaml
import json


def add_pod_to_config(json_filename ,yaml_filename):
    file = open(json_filename)
    data = json.load(file)
    print(data)

    # Create a combined config file for both type for both type of pods

    pass

if __name__ == '__main__':
    add_pod_to_config('config/structure.json', 'config.yaml')