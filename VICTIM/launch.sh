#!/bin/bash

output_file="$1.txt"

for ((i=0; i<=2; i++))
do
  for ((j=2; j>0; j--))
  do
    echo "[+] wait $j "
    sleep 1
  done
  echo "[+] Start"
  ./perf stat -e l3_misses python3 ML.py 2> "$output_file" >/dev/null 
  cat "$output_file" | grep "l3_misses"
  echo "[+] Ended"
done
