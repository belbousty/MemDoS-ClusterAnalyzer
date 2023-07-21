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

    if [ "num_nodes" -ne $0 ]
    then 
        echo "[+] Starting Minikube with $0 nodes, $1 cpus $2 MB of memory each"
        minikube start --nodes $0 --cpus $1 --memory $2
    else
        echo "[+] Minikube is already runing with 2 nodes"
    fi
fi

# build or pull necessary images
if docker image inspect ubuntu &> /dev/null
then
    echo "[+] ubuntu docker image already exists"
else 
    docker pull ubuntu
fi

if docker image inspect hibench:0.0.1 &> /dev/null; then
    echo "[+] hibench docker imagee already exists"
else
    echo "building hibench docker image"
    git clone https://github.com/lmendiboure/Memory_DoS_Project.git && cd Memory_DoS_Project/Hi-Bench-Container
    DOCKER_BUILDKIT=0 docker build -t hibench:0.0.1 . && cd ../../
fi

# load necessary image
if minikube image ls | grep "docker.io/library/ubuntu"
then
    echo "[+] ubuntu minikube already exists"
else 
    minikube image load ubuntu
fi

if minikube image ls | grep "docker.io/library/hibench:0.0.1"
then
    echo "[+] hibench:0.0.1 minikube already exists"
else 
    minikube image load ubuntu
fi


# applying configuration
echo "[+] Creating Pods from config.yaml"
kubectl apply -f config/config.yaml

echo "[+] Finished"
