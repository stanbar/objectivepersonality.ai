#!/bin/bash

echo "Running benchmarks..."

echo "---------Centroids----------"
poetry run python objectivepersonality_ai/benchmarks/centroids.py

echo "---------Neural-Network----------"
poetry run python objectivepersonality_ai/benchmarks/neural_network.py

echo "---------Proto-Networks----------"
poetry run python objectivepersonality_ai/benchmarks/proto_networks.py