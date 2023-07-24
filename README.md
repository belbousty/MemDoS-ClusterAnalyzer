This repository helps launching a N node cluster with x number of attackers an y number of victims in each node

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
    python3 main.py [POD_NAME] [NEW_POD_NAME] [DEST_NODE]
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
