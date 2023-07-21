#!/bin/bash

minikube delete && minikube start --cpus=6 --memory=10000 --disk-size=25g --namespace=k8s-bigdata

. "$(dirname "$0")/functions.sh"

RED='\033[0;31m'
PLAIN='\033[0m'
ERR_TAG="[ ${RED}ERROR${PLAIN} ]"
WORKLOAD=$1
BENCHMARK=$2
INPUT_SIZE=$3

if [[ ! $WORKLOAD ]]; then
	echo -e "${ERR_TAG} Missing WORKLOAD parameter"
	exit 1
fi

if [[ ! $BENCHMARK ]]; then
	echo -e "${ERR_TAG} Missing BENCHMARK parameter"
	exit 1
fi

if [[ ! $INPUT_SIZE ]]; then
	echo -e "${ERR_TAG} Missing INPUT_SIZE parameter"
	exit 1
fi

###################
## START CLUSTER ##
###################
apply kubernetes/cluster.yml

wait_pods

sleep 10

################
## NETWORKING ##
################
#add_host namenode
#add_host historyserver
#add_host datanodes
#add_host resourcemanager
set_benchmark_input_size $INPUT_SIZE
set_executor_memory "15g"
set_executor_cores "4"

#########################
## CREATING INPUT DATA ##
#########################
prepare $WORKLOAD $BENCHMARK
