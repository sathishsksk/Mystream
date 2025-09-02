#!/bin/bash

# Create data directory
mkdir -p data/files data/thumbnails

# Start with Docker Compose
docker-compose up -d

# Show logs
docker-compose logs -f
