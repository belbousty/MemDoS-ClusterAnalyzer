#!/bin/bash

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
    local node_count=$(kubectl get nodes | wc -l)
    echo "$(($node_count - 2))"
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
