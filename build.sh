#!/bin/bash

re='^[0-9]+$'
if [ $#  -ne  3 ]
then
    echo -e "[-] Please specify number of nodes, cpus and the size of the memory for each node\ ./build [NUM_NODES] [NUM_CPUS] [MEMORY]"
    exit
fi
for arg in $@
do 
    if ! [[ $arg =~ $re ]]
    then 
        echo -e "[-] Please enter an integer instead of '$arg'"
        exit
    fi
done 

# Create a 2-node cluster
if ! minikube status &> /dev/null
then
    echo "[+] Checking Minikube existing nodes"
    num_nodes=$(minikube node list | wc -l)
    if [ $num_nodes -ne $[$1+2] ]
    then 
        echo "[+] Starting Minikube with $1 nodes, $2 cpus $3 MB of memory each"
        minikube start --nodes "$1" --cpus "$2" --memory "$3"
    else
        echo "[+] Minikube is already runing with $1 nodes"
    fi
fi

# build or pull necessary images
if docker image inspect attacker:0.0.1 &> /dev/null
then
    echo "[+] attacker docker iamge already exists"
else 
    echo "building attacker docker image"
    cd attacker && DOCKER_BUILDKIT=0 docker build -t attacker:0.0.1 . 
    cd ../
fi

if docker image inspect hibench:0.0.1 &> /dev/null; then
    echo "[+] hibench docker image already exists"
else
    echo "building hibench docker image"
    cd hibenchPod && DOCKER_BUILDKIT=0 docker build -t hibench:0.0.1 . && cd ../
fi

# load necessary images
if minikube image ls | grep "docker.io/library/attacker:0.0.1"
then
    echo "[+] attacker:0.0.1 minikube already exists"
else
    echo "[+] Loading attacker image to minikube"
    minikube image load attacker:0.0.1
fi

if minikube image ls | grep "docker.io/library/hibench:0.0.1"
then
    echo "[+] hibench:0.0.1 minikube already exists"
else 
    echo "[+] Loading hibench image to minikube"
    minikube image load hibench:0.0.1
fi