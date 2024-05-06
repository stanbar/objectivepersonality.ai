#!/bin/bash

echo "Running benchmarks..."

echo "---------Centroids----------"
python3 objectivepersonality_ai/benchmarks/centroids.py

echo "---------Neural-Network----------"
python3 objectivepersonality_ai/benchmarks/neural_network.py

echo "---------Proto-Networks----------"
python3 objectivepersonality_ai/benchmarks/proto_networks.py