# Distribution usually used with HiBench

FROM ubuntu:18.04 

# Define required environment variables 
ENV MAVEN_HOME="/opt/apache-maven-3.2.5"
ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
ENV HADOOP_HOME="/opt/hadoop-3.2.4"

# Required for HDFS
ENV HDFS_NAMENODE_USER="root"
ENV HDFS_DATANODE_USER="root" 
ENV HDFS_SECONDARYNAMENODE_USER="root"
ENV YARN_RESOURCEMANAGER_USER="root"
ENV YARN_NODEMANAGER_USER="root"

# Copy required Files

ADD instals/docker-config.sh /root/docker-config.sh
ADD instals/run_dfs.sh /root/run_dfs.sh
ADD conf/hibench.conf /root/hibench.conf
ADD conf/hadoop.conf /root/hadoop.conf

# Enable Files Execution
RUN chmod 777 /root/docker-config.sh
RUN chmod 777 /root/run_dfs.sh

# Run Basic Install
RUN /root/docker-config.sh


# installing perf binary
RUN apt update && apt upgrade 
RUN apt install linux-tools && apt install linux-tools-generic
RUN cp /usr/lib/linux-tools/4.15.0-213-generic/perf /root

