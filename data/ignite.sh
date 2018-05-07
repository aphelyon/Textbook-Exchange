#!/usr/bin/env bash
docker exec spark-master bash /tmp/data/mysql-install.sh
docker exec spark-worker bash /tmp/data/mysql-install.sh
while [ true ]
do
    docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/spark.py
    sleep 90
done