#!/bin/bash

source ./functions.sh


test_files=$(ls -1 test | cut -d '.' -f1)
for test in $test_files
do 
    echo "[+] Starting Experiment $test"
    necessary_nodes=$(jq -r ".nodes" test/$test.json)
    node_num=$(count_minikube_nodes)
    if [ $necessary_nodes != $node_num ]
    then 
        echo "[-] Inappropriate number of nodes."
        exit
    fi

    echo "[+] Launching test"
    echo "[+] Creating Pods from test/$test.json"

    duration=$1
    python3 src/structure.py --json test/$test.json --tool $2
    kubectl apply -f config/config.yaml
    apply_experience $duration $test

    echo "[+] Finished"
done 