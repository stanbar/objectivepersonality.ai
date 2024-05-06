#!/bin/bash

echo "Running benchmarks..."

echo "---------Centroids----------"
python3 benchmark_centroids.py

echo "---------Neural-Network----------"
python3 benchmark_neural_network.py

echo "---------Proto-Networks----------"
python3 benchmark_proto_networks.py