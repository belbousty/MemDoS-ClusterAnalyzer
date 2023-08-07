#!/bin/bash

function count_minikube_nodes() {
    local node_count=$(minikube node list | wc -l)
    echo "$((node_count))"
}

function files_in_test() {
    if [ -d test ]
    then

        for file in test/* 
        do 
            echo "$(basename "$file")"
        done
    fi
}

function apply_experience() {
    duration=$1
    
    echo "[+] Starting the experience with attacks"
    python3 src/launch.py --duration $1
    echo "[+] Experience ended with attacks"

    echo "[+] Starting the experience with attacks"
    python3 src/launch.py --duration $1 --no-attacks
    echo "[+] Experience ended with attacks"

    echo "[+] Showing figures"
    python3 src/figures.py
}

function adjust_nodes() {
    necessary_nodes=$1
    num_nodes=$2
    needed_nodes=$(($num_nodes - $necessary_nodes))
    if [ $needed_nodes -lt 0 ]
    then
        echo "[+] Adding necessary nodes"
        for ((i = 1; i <= -needed_nodes; i++)) 
        do 
            minikube node add
        done
    else
        node_list=$(minikube node list | cut -f1) 
        nodes_to_delete=$(($num_nodes - $necessary_nodes))
        nodes_to_delete_list=$(echo "$node_list" | tail -n $nodes_to_delete)

        for node in $nodes_to_delete_list
        do
            echo "[+] deleting $node"
            minikube node stop $node
            minikube node delete $node
        done
    fi
}


if [ $# == 1 ]
then
    exit
    echo "[+] Creating Pods from config.yaml"

    python3 src/structure.py --json structure.json
    kubectl apply -f config/config.yaml

    echo "[+] Finished"
    
    apply_experience $1

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

    apply_experience $2
else
    echo "[-] Enter the correct parameters"
fi