#!/bin/bash

re='^[0-9]+$'
if [ $#  -ne  3 ] && [ $# -ne 1 ] 
then
    echo -e "[-] To use minikube, specify number cpus and the size of the memory for each node\ ./build [NUM_NODE] [NUM_CPUS] [MEMORY] "
    echo -e "[-] To use kind, specify number of nodes ./build [NUM_NODE]"
    exit
fi

tool='minikube'
if [ $# -eq 1 ]
then 
    tool='kind'
fi

for arg in $@
do 
    if ! [[ $arg =~ $re ]]
    then 
        echo -e "[-] Please enter an integer instead of '$arg'"
        exit
    fi
done 


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

if docker image inspect cri-rm-node:latest &> /dev/null
then
    echo "[+] cri-rm-node docker image already exists"
else
    echo "building cri-rm-node docker image"
    cd node-deployment && DOCKER_BUILDKIT=0 docker build -t cri-rm-node . && cd ../
fi


if [[ $tool == 'minikube' ]]
then
    minikube delete
    if ! minikube status &> /dev/null
    then 
        echo "[+] Starting Minikube with $1 nodes, $2 cpus $3 MB of memory each"
        minikube start --nodes $(($1+1)) --cpus "$2" --memory "$3"
    else
        echo "[+] Minikube is already runing"
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
fi

if [[ $tool == 'kind' ]]
then 
    N="$1"
    if ! [[ "$N" =~ ^[1-9][0-9]*$ ]]; then
    echo "Please provide a positive integer for the number of nodes."
    exit 1
    fi

cat <<EOF > nodes.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
EOF
for ((i=1; i<=N; i++)); do
echo "  - role: worker" >> nodes.yaml
done
        
    kind delete cluster --name cri-rm-cluster
    kind create cluster --config nodes.yaml --name cri-rm-cluster --image cri-rm-node

    kind load docker-image attacker:0.0.1 --name cri-rm-cluster
    kind load docker-image hibench:0.0.1 --name cri-rm-cluster    
fi