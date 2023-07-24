#!/bin/bash
# Format File System for HDFS

chown -R "$(whoami):" "$HADOOP_HOME"

/opt/hadoop-3.2.4/bin/hdfs namenode -format

/opt/hadoop-3.2.4/sbin/start-dfs.sh
