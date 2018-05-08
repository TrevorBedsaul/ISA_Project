#!/usr/bin/env bash
bin/spark-class org.apache.spark.deploy.master.Master -h spark-master &
while true
do
    bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/spark_job.py
    sleep 60
done
