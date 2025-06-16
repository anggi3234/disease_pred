#!/bin/bash

# Disease Prediction App Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 Starting Disease Prediction App Deployment..."
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Stop and remove existing containers
echo "🔄 Stopping existing containers..."
docker-compose down --remove-orphans || true

# Build and start the application
echo "🏗️  Building and starting the application..."
docker-compose up --build -d

# Wait for the application to be ready
echo "⏳ Waiting for application to be ready..."
sleep 10

# Check if the application is running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Application deployed successfully!"
    echo "📱 Access the application at: http://localhost:8501"
    echo "📊 Health check: http://localhost:8501/_stcore/health"
    echo ""
    echo "🔧 Useful commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop app: docker-compose down"
    echo "   - Restart: docker-compose restart"
else
    echo "❌ Deployment failed. Check logs with: docker-compose logs"
    exit 1
fi

echo "✨ Deployment completed!"

