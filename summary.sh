#!/usr/bin/env bash
# Copies files from a running container to host results/ and removes the container.
set -e
CONTAINER=${1:-}
if [ -z "$CONTAINER" ]; then
  echo "Usage: ./summary.sh <container_id_or_name>"
  exit 1
fi
mkdir -p results
docker cp "$CONTAINER":/app/pipeline/data_raw.csv results/ || true
docker cp "$CONTAINER":/app/pipeline/data_preprocessed.csv results/ || true
docker cp "$CONTAINER":/app/pipeline/insight1.txt results/ || true
docker cp "$CONTAINER":/app/pipeline/insight2.txt results/ || true
docker cp "$CONTAINER":/app/pipeline/insight3.txt results/ || true
docker cp "$CONTAINER":/app/pipeline/summary_plot.png results/ || true
docker cp "$CONTAINER":/app/pipeline/clusters.txt results/ || true
docker stop "$CONTAINER" || true
docker rm "$CONTAINER" || true
echo "Results copied to ./results/ and container removed."
