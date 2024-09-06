#!/bin/bash

# Build the base images from which are based the Dockerfiles
# then Startup all the containers at once
docker build -t hadoop-base docker/hadoop/hadoop-base && \
docker build -t airflow/stock-app docker/spark/notebooks/stock_transform && \
docker compose up -d --build
