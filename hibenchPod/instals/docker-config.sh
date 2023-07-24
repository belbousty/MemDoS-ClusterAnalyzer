#!/bin/bash

apt-get update

# Install utils: python + bc + git + wget + nano + dstat
apt-get install dstat apt-utils
apt install python bc git wget nano -y


# Install Maven (+Clean Useless Files)

wget https://archive.apache.org/dist/maven/maven-3/3.2.5/binaries/apache-maven-3.2.5-bin.tar.gz
tar xvfz apache-maven-3.2.5-bin.tar.gz
cp -r apache-maven-3.2.5 "$MAVEN_HOME"
rm -rf apache-maven-3.2.5 apache-maven-3.2.5-bin.tar.gz

# Install Java 8

apt install openjdk-8-jdk -y

# Install Hadoop (+Clean Useless Files)
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.2.4/hadoop-3.2.4.tar.gz
tar xvf hadoop-3.2.4.tar.gz
cp -r hadoop-3.2.4 "$HADOOP_HOME"
rm -rf hadoop-3.2.4 hadoop-3.2.4.tar.gz
echo "export JAVA_HOME=\"/usr/lib/jvm/java-8-openjdk-amd64\"" >> "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"  # Add Java Info within Hadoop


# Set HDSF Info (Not Should be made dynamically)
 
printf '<configuration>\n  <property>\n    <name>fs.defaultFS</name>\n    <value>hdfs://localhost:9000</value>\n  </property>\n</configuration>\n' > "$HADOOP_HOME/etc/hadoop/core-site.xml" 
printf '<configuration>\n  <property>\n    <name>dfs.replication</name>\n    <value>1</value>\n  </property>\n</configuration>\n' > "$HADOOP_HOME/etc/hadoop/hdfs-site.xml"
 
 # Install SSH 

apt-get install keychain openssh-server -y

# Generate RSA Keys and store it
mkdir /root/.ssh
ssh-keygen -C "" -P "" -f "/root/.ssh/id_rsa"
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys

# Download HiBench 

git clone https://github.com/Intel-bigdata/HiBench.git

# Build HiBench

cd HiBench
$MAVEN_HOME/bin/mvn -Phadoopbench -Dspark=2.4 -Dscala=2.11 clean package

# Configure HiBench with Specific Achitecture - Local Hadoop Cluster (NOTE : HADOOP PORT IS A HARD CODED VALUE : 9000)
rm /HiBench/conf/hibench.conf
mv /root/hibench.conf /HiBench/conf/hibench.conf
mv /root/hadoop.conf /HiBench/conf/hadoop.conf 
