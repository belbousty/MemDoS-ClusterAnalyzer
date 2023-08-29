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
        adjust_nodes $necessary_nodes $node_num
    fi

    echo "[+] Launching test"
    echo "[+] Creating Pods from test/$test.json"

    python3 src/structure.py --json test/$test.json
    kubectl apply -f config/config.yaml
    #apply_experience $2 $1

    echo "[+] Finished"
    exit
done 