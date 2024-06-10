#!/bin/bash

echo "Running benchmarks..."

echo "---------Centroids----------"
python3 benchmark_centroids.py

echo "---------Weighted-Centroids----------"
python3 benchmark_weighted_centroids.py

echo "---------Neural-Network----------"
python3 benchmark_neural_network.py

echo "---------Proto-Networks----------"
python3 benchmark_proto_networks.py

echo "---------Random-Forest----------"
python3 benchmark_random_forest.py