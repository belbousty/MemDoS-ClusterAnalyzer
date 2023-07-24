This repository helps launching a N node cluster with x number of attackers an y number of victims in each node

# Launch

To run it with Minikube:
```console
# Build the cluster
    ./build.sh [NUM_NODES] [NODE_NUM_CPUS] [NODE_MEMORY_SIZE]

```
# Fixed issues
Allowing perf stat capability:
```console
    # On the local machine
    echo -1 > /proc/sys/kernel/perf_event_paranoid
```