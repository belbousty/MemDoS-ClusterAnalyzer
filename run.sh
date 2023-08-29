#!/bin/bash

source ./functions.sh

if [ $# == 1 ]
then
    necessary_nodes=$(jq -r ".nodes" structure.json)
    node_num=$(count_minikube_nodes)
    if [ $necessary_nodes != $node_num ]
    then 
        echo "[-] Inappropriate number of nodes."
        adjust_nodes $necessary_nodes $node_num
    fi
    echo "[+] Creating Pods from config.yaml"

    python3 src/structure.py --json structure.json
    kubectl apply -f config/config.yaml

    echo "[+] Finished"
    
    #apply_experience $1 

elif [ $# == 2 ]
then
    necessary_nodes=$(jq -r ".nodes" test/$1.json)
    node_num=$(count_minikube_nodes)
    if [ $necessary_nodes != $node_num ]
    then 
        echo "[-] Inappropriate number of nodes."
        adjust_nodes $necessary_nodes $node_num
    fi

    echo "[+] Launching test"
    echo "[+] Creating Pods from test/$1.json"

    python3 src/structure.py --json test/$1.json
    kubectl apply -f config/config.yaml

    echo "[+] Finished"

    apply_experience $2 $1
else
    echo "[-] Enter the correct parameters"
fi