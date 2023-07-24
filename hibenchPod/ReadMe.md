# Objective

Docker container that can run different HiBench workloads (Hadoop workloads).

# Required tools on your machine

Docker, Kubernetes, MiniKube

# Deployment Procedure

To run it with Minikube:
```console
# Start minikube
# Note: Memory and CPU could be configured depending on your machine and requirements

minikube start --memory 32000 --cpus 2 --nodes

# Build image
# Note: DOCKER_BUILDKIT=0 could be required to see the build state
# Note: name used for the image should also be specified in the hibench-deployment.yaml file
# Not required if the image is already loaded within your Docker images (docker image ls)

DOCKER_BUILDKIT=0 docker build -t hibench:0.0.1 .

# Load image within Minikube

minikube image load hibench:0.0.1

# Define a new namespace that will be used to deploy the pod
# Note: a specific configuration is used to increase the amount of resource that can be used by this pod: avoid potentiel error 137 and enables both Hadoop and HiBench operation

kubectl create namespace qos-hibench

# Run in minikube
 
kubectl apply -f hibench-deployment.yaml --namespace=qos-hibench

# Access Shell
kubectl exec --namespace=qos-hibench hibench-pod --stdin --tty -- /bin/bash

```
Potential useful commands
  1. kubectl get pods --namespace=qos-hibench
  2. kubectl delete pods hibench-pod --namespace=qos-hibench
  3. kubectl get pod hibench-pod --namespace=qos-hibench --output=yaml
  4. minikube delete
  5. kubectl get node minikube -o jsonpath='{.status.capacity}'
  6. minikube image ls
  7. minikube dashboard #to visualize nodes (after minikube addons enable metrics-server) 

# Use

`Note : Within the HiBench folder of the pod (exec + cd...)`

To run workloads (once pod started) - Could be directly integrated within RUN to directly obtain result and automatically stop the pod once results are obtained:
  1. ```bin/workloads/micro/wordcount/prepare/prepare.sh```
  2. ```bin/workloads/micro/wordcount/hadoop/run.sh```

To display results:

-> <HiBench_Root>/report/hibench.report
-> <workload>/hadoop/bench.log: Raw logs on client side.
-> <workload>/hadoop/monitor.html: System utilization monitor results.
-> <workload>/hadoop/conf/<workload>.conf: Generated environment variable configurations for this workload.

Note: To change the input data size, you can set hibench.scale.profile in conf/hibench.conf
Note : Change (hibench.default.map.parallelism,hibench.default.shuffle.parallelism) in conf/hibench.conf to control the parallelism.


# Known Errors

If an error 137 occurs during once the pod is launched, it could be related to the limited memory resources allocated to Docker Containers.

To deal with that, it would be necessary :

  1. To modify the `/etc/docker/daemon.json` file to increase the amout of resources that are memory allocated to Docker containers (initially 10Go). The following lines should be added:

       a. "storage-driver": "devicemapper",
       b. "storage-opts": ["dm.basesize=40G"]
  
  2. Restart the docker deamon: `sudo service docker restart`
