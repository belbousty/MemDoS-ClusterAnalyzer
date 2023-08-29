#!/bin/bash

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

function apply_experience() {
    duration=$1
    filename=$2

    echo "[+] Starting the experience with attacks"
    python3 src/launch.py --duration $duration --experiment $filename
    echo "[+] Experience ended with attacks"

    echo "[+] Starting the experience without attacks"
    python3 src/launch.py --duration $duration --experiment $filename --no-attacks 
    echo "[+] Experience ended without attacks"

    echo "[+] Showing figures"
    python3 src/figures.py --experiment $filename
}

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