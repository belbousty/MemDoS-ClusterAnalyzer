# 2-node cluster creation
if ! minikube status &> /dev/null; then

    echo "[+] Checking Minikube existing nodes"
    num_nodes=$(minikube node list | wc -l)

    if [ "num_nodes" -ne 2 ]; then
        echo "Starting Minikube with 2 nodes, 3 cpus 32GB of memory each"
        minikube start --nodes 2 --cpus 3 --memory 32000
    else
        echo "Minikube is already runing with 2 nodes"
    fi
fi
# build or pull necessary images

docker pull ubuntu
if docker image inspect hibench:0.0.1 &> /dev/null; then
    echo "hibench docker imagee already exists"
else
    echo "building hibench docker image"
    cd Memory_DoS_Project/Hi-Bench-Container &&  DOCKER_BUILDKIT=0 docker build -t hibench:0.0.1 . && cd ../../
fi

# load necessary image
if minikub image ls | grep "docker.io/ubuntu"; then
    echo "[+] ubuntu minikube already exists"
else 
    minikube image load ubuntu
fi
if minikub image ls | grep "docker.io/hibench:0.0.1"; then
    echo "[+] hibench:0.0.1 minikube already exists"
else 
    minikube image load ubuntu
fi

#minikube image load hibench:0.0.1

# applying configuration
echo "[+] Creating Pods from config.yaml"

kubectl apply -f config.yaml

