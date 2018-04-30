#!/usr/bin/env bash
docker exec spark-master apt-get update &&
docker exec spark-master apt-get install python3-dev libmysqlclient-dev -y &&
docker exec spark-master apt-get install python-pip -y &&
docker exec spark-master pip install mysqlclient &&
docker exec spark-master apt-get install python-mysqldb
docker exec spark-worker apt-get update &&
docker exec spark-worker apt-get install python3-dev libmysqlclient-dev -y &&
docker exec spark-worker apt-get install python-pip -y &&
docker exec spark-worker pip install mysqlclient &&
docker exec spark-worker apt-get install python-mysqldb
docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/spark.py
