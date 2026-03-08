#!/bin/bash

echo "Starting deployment..."


# Build and start all containers
docker compose -f docker-compose.prod.yml up --build -d


echo "Waiting for containers to start..."
sleep 5

# Show status
docker compose -f docker-compose.prod.yml ps


echo "Deployment complete!"
echo "App running at: https://localhost"