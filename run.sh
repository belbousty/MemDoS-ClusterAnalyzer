#!/bin/bash

# Create a function that delete existing pods, and nodes if needed


# applying configuration
if [ $# == 0 ]
then
    echo "[+] Creating Pods from config.yaml"

    python3 src/structure.py --json structure.json
    kubectl apply -f config/config.yaml

    echo "[+] Finished"

elif [ $# == 2 ]
then
    echo "[+] Launching the 1-node test"
    echo "[+] Creating Pods from test/config/$1/$2/structure.json"

    python3 src/structure.py --json test/config/$1/$2/structure.json
    kubectl apply -f config/config.yaml

    echo "[+] Finished"
else 
    echo "[-] Please execute without any parameters or specify the test and the attack type"
fi