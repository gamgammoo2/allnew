#!/bin/bash

#default mongodb deamon stop.
systemctl stop mongod

#stop shard
./stop_shard.sh

# remove data directory
if [ -d data ]; then ##-d : 디렉토리를 구성하면~
    rm -rf ./data
fi

#config Server
mkdir -pv /shard/data/configdb
mkdir -pv /shard/data/logs
touch /shard/data/logs/configsvr.log

mongod --config /shard/mongodConfig.conf &
sleep 5s

#router Server
touch /shard/data/logs/mongorouter.log

mongos --config /shard/mongodRouter.conf &
sleep 5s

#shard1 Server
mkdir -pv /shard/data/shard1db
touch /shard/data/logs/shard1.log

mongod --config /shard/mongodShard1.conf &
sleep 5s

#shard2 Server
mkdir -pv /shard/data/shard2db
touch /shard/data/logs/shard2.log

mongod --config /shard/mongoShard2.conf &
sleep 5s

#process status
ps -ef | grep mongo
sleep 5s

#netstatus
netstat -ntlp