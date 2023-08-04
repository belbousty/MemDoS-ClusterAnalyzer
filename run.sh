#!/bin/bash

# Create a function that delete existing pods, and nodes if needed
function count_minikube_nodes() {
    local node_count=$(minikube node list | wc -l)
    echo "$((node_count))"
}

function node_number() {
    file=$1
    if [ $file == "one-node" ] 
    then 
        echo 1
    elif [ $file == "two-nodes" ]
    then 
        echo 2
    elif [ $file == "three-nodes" ]
    then
        echo 3
    else 
        echo "[-] The name of the test is wrong"
        exit
    fi
}
# applying configuration
if [ $# == 1 ]
then
    exit
    echo "[+] Creating Pods from config.yaml"

    python3 src/structure.py --json structure.json
    kubectl apply -f config/config.yaml

    echo "[+] Finished"
    
    echo "[+] Starting the experience with attacks"
    python3 src/launch.py --duration $1
    echo "[+] Experience ended with attacks"

    echo "[+] Starting the experience with attacks"
    python3 src/launch.py --duration $1 --no-attacks
    echo "[+] Experience ended with attacks"

    echo "[+] Showing figures"
    python3 src/figures.py

elif [ $# == 3 ]
then
    necessary_nodes=$(node_number $1)
    node_num=$(count_minikube_nodes)

    if [ $necessary_nodes != $node_num ]
    then 
        echo "[+] Inappropriate number of nodes. Please restart the cluster and rebuild properly"
        exit
    fi
    echo "[+] Launching the $1 test"
    echo "[+] Creating Pods from test/config/$1/$2/structure.json"

    python3 src/structure.py --json test/config/$1/$2/structure.json
    kubectl apply -f config/config.yaml

    echo "[+] Finished"

    echo "[+] Starting the experience with attacks"
    python3 src/launch.py --duration $3
    echo "[+] Experience ended with attacks"

    echo "[+] Starting the experience with attacks"
    python3 src/launch.py --duration $3 --no-attacks
    echo "[+] Experience ended with attacks"

    echo "[+] Showing figures"
    python3 src/figures.py
else
    echo "[-] Please execute without any parameters or specify the test and the attack type"
fi