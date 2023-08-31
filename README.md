This repository helps launching a N node cluster with x number of attackers an y number of victims in each node, extracting statistics on LLC usage and applications' execution time and producing graphs in order to compare results of a "Live Attack" and "Non-Attack" Simulation

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
    ./run.sh [DURATION] minikube
    ./run.sh [FILENAME] [DURATION] minikube , the file should be without extension and stored in 'test' directory
# Running all test
    ./run_all.sh [DURATION] minikube
```
To run it using KinD:
```console
# Build the cluster
    ./build.sh  [NODE_NUM_CPUS]
# Run the experiment using structure.json for pods creation
    ./run.sh [DURATION] kind
    ./run.sh [FILENAME] [DURATION] kind , the file should be without extension and stored in 'test' directory
# Running all test
    ./run_all.sh [DURATION] kind
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
    
# At the end, perf results will be stored in stats in both csv and text format 
# And figures of these results are stored in "figures" 
```
# Migration 
```console
# Migrate pod to node
    python3 src/migrate.py [POD_NAME] [NEW_POD_NAME] [DEST_NODE]

```
# Start the experiment 
```console
# launching experiment
    python3 src/launch.py  --duration [DURATION] --experiment [FILENAME], the file should be without extension and stored in 'test' directory

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
    pip install matplotlib
    pip install pandas
# Installing perf
    sudo apt install linux-tools
    sudo apt install jq
```
# Fixed issues
Allowing perf stat capability:
```console
# On the local machine as root (mandatory for perf)
    echo -1 > /proc/sys/kernel/perf_event_paranoid
```
