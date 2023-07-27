This repository helps launching a N node cluster with x number of attackers an y number of victims in each node
# Specify pods in structure.json
```console
# You should specify exactly the values required in structure.json
# It is necessary for "type" to be either "attacker" or "victim" 
# The image is either  "docker.io/library/attacker:0.0.1" or "docker.io/library/hibench:0.0.1"
# To check minikube images:  minikube image list
# Example:  
    {
        "type": "attacker",
        "name": "attacker00",
        "nodeName": "minikube",
        "attackType": "llc",
        "duration": "2", ## The attack will take 2 minutes
        "start": "1", ## The attack will start exactly after the first minute of the total duration of the experiment
        "image" : "docker.io/library/attacker:0.0.1",
        "limits" : [
            {
            "cpu": "2000m",
            "memory": "32000Mi"    
            }
        ],
        "requests" :[
            {
                "cpu": "800m",
                "memory": "2000Mi"    
            }
        ]
    }
# AttackType should be either 'llc' or 'lock'
# Example for the victim: 
    {
        "type": "victim",
        "name": "victim00",
        "nodeName": "minikube",
        "workload": "ml", ## Specify the workload 
        "benchmark": "kmeans", ## Specify the benchmark
        "image" : "docker.io/library/hibench:0.0.1",
        "limits" : [
            {
            "cpu": "2000m",
            "memory": "32000Mi"    
            }
        ],
        "requests" :[
            {
                "cpu": "800m",
                "memory": "4000Mi"   
            }
        ]
    }
check "https://github.com/Intel-bigdata/HiBench/" for workloads and benchmarks
```

# Launch

To run it with Minikube:
```console
# Build the cluster
    ./build.sh [NUM_NODES] [NODE_NUM_CPUS] [NODE_MEMORY_SIZE]
# Example : creating 2-node cluster with 3 cpus and 20000MB each
    ./build.sh 2 3 20000
```

# Migration 
```console
# Migrate pod to node
    python3 src/main.py [POD_NAME] [NEW_POD_NAME] [DEST_NODE]
```
# Start the experiment 
```console
# launching experiment in 2 minutes
    python3 src/launch.py  --duration 2
```
# Version Requirements
```console
## Docker version 20.10.24
## minikube version: v1.30.1
## Python 3.8.10
# Install python libraries
    pip install json
    pip install pyyaml
# Installing perf
    sudo apt install linux-tools
```
# Fixed issues
Allowing perf stat capability:
```console
# On the local machine
    echo -1 > /proc/sys/kernel/perf_event_paranoid
```
