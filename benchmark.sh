#!/bin/bash

echo "Running benchmarks..."

echo "---------Centroids----------"
python objectivepersonality_ai/benchmarks/centroids.py

echo "---------Neural-Network----------"
python objectivepersonality_ai/benchmarks/neural_network.py

echo "---------Proto-Networks----------"
python objectivepersonality_ai/benchmarks/proto_networks.py