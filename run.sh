#!/bin/bash

source ./functions.sh

if [ $# == 2 ]
then
    necessary_nodes=$(jq -r ".nodes" structure.json)
    node_num=$(count_minikube_nodes)
    if [ $necessary_nodes != $node_num ]
    then 
        echo "[-] Inappropriate number of nodes."
        echo "[-] Please rebuild with the appropriate number"
        exit
    fi
    echo "[+] Creating Pods from config.yaml"

    python3 src/structure.py --json structure.json --tool $2
    kubectl apply -f config/config.yaml

    echo "[+] Finished"
    
    #apply_experience $1 structure

elif [ $# == 3 ]
then
    necessary_nodes=$(jq -r ".nodes" test/$1.json)
    node_num=$(count_minikube_nodes)
    if [ $necessary_nodes != $node_num ]
    then 
        echo "[-] Inappropriate number of nodes."
        echo "[-] Please rebuild with the appropriate number"
        exit
    fi

    echo "[+] Launching test"
    echo "[+] Creating Pods from test/$1.json"

    python3 src/structure.py --json test/$1.json --tool $3
    kubectl apply -f config/config.yaml

    echo "[+] Finished"

    #apply_experience $2 $1
else
    echo "[-] Enter the correct parameters"
fi