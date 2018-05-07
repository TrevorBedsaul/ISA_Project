#!/usr/bin/env bash

while true
do
    bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/spark_job.py
    sleep 60
done
