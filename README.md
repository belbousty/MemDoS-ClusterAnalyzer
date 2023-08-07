This repository helps launching a N node cluster with x number of attackers an y number of victims in each node
# Specify pods in structure.json
```console
# You should specify exactly the values required in structure.json
# AttackType should be either 'llc' or 'lock'
# Example:
    {
    "nodes": "2
    "attackers": [ 
        {
            "node": "1",
            "attackType": "llc",
            "duration": "15",
            "start": "0"
        },
        {
            "node": "2",
            "attackType": "lock",
            "duration": "15",
            "start": "0"
        }],

    "victims": [{
            "node": "1",
            "workload": "ml",
            "benchmark": "kmeans"
        },
        {
            "node": "2",
            "workload": "ml",
            "benchmark": "kmeans"
        }]
    }

# NB : in case other changes are required, please refer to  config/config.yaml
# check "https://github.com/Intel-bigdata/HiBench/" for workloads and benchmarks
```

# Launch

To run it with Minikube:
```console
# Build the cluster
    ./build.sh  [NODE_NUM_CPUS] [NODE_MEMORY_SIZE]
# Example : creating 1 node cluster with 3 cpus and 20000MB each
    ./build.sh 3 20000
# Run the experiment
    ./run.sh [Duratioon]
# make sure the duration is superior than the maximum attack duration
```

# Tests
We provided 3 tests each with different node characteristics and type of attacks.
```console
# If the number of node or memory specifics of the existing cluster does not match those of the chosen test
# Then restart with the appropriate spec
# Otherwise: 
    ./run.sh [TEST] [DURATION]
    
    [TEST]: name of the json file (without the extension)
```
# Migration 
```console
# Migrate pod to node
    python3 src/migrate.py [POD_NAME] [NEW_POD_NAME] [DEST_NODE]

```
# Start the experiment 
```console
# launching experiment
    python3 src/launch.py  --duration [DURATION]

# launching experiment without any attacks (without changing the json file)
    python3 src/launch.py  --duration [DURATION] --no-attacks
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
# On the local machine as root
    echo -1 > /proc/sys/kernel/perf_event_paranoid
```
