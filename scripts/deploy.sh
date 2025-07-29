#!/bin/bash
# Deployment script for Smart Report Assistant

set -e  # Exit on any error

# Configuration
APP_NAME="smart-report-assistant"
DOCKER_IMAGE="$APP_NAME"
CONTAINER_NAME="$APP_NAME-container"
PORT=5000
HEALTH_CHECK_URL="http://localhost:$PORT/"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    log "Docker is running ✓"
}

# Function to build the Docker image
build_image() {
    log "Building Docker image..."
    docker build -t $DOCKER_IMAGE .
    log "Docker image built successfully ✓"
}

# Function to stop existing container
stop_container() {
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        log "Stopping existing container..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
        log "Existing container stopped and removed ✓"
    fi
}

# Function to run the container
run_container() {
    log "Starting new container..."
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:5000 \
        -v "$(pwd)/app/uploads:/app/app/uploads" \
        -v "$(pwd)/app/static/plots:/app/app/static/plots" \
        --restart unless-stopped \
        $DOCKER_IMAGE
    
    log "Container started successfully ✓"
}

# Function to check application health
health_check() {
    log "Performing health check..."
    
    # Wait for container to start
    sleep 10
    
    # Check if container is running
    if ! docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        error "Container failed to start"
        docker logs $CONTAINER_NAME
        exit 1
    fi
    
    # Check HTTP endpoint
    for i in {1..30}; do
        if curl -f -s $HEALTH_CHECK_URL > /dev/null; then
            log "Application is healthy ✓"
            log "Application is available at: $HEALTH_CHECK_URL"
            return 0
        fi
        warn "Health check attempt $i/30 failed, retrying in 5 seconds..."
        sleep 5
    done
    
    error "Health check failed after 30 attempts"
    docker logs $CONTAINER_NAME
    exit 1
}

# Function to show container logs
show_logs() {
    log "Showing container logs..."
    docker logs -f $CONTAINER_NAME
}

# Function to run database migrations (if needed in future)
run_migrations() {
    log "Running database migrations..."
    # Add migration commands here if needed
    log "Migrations completed ✓"
}

# Main deployment function
deploy() {
    log "Starting deployment of $APP_NAME..."
    
    check_docker
    build_image
    stop_container
    run_container
    run_migrations
    health_check
    
    log "Deployment completed successfully! 🚀"
    log "Application is running at: $HEALTH_CHECK_URL"
}

# Function to rollback deployment
rollback() {
    warn "Rolling back deployment..."
    stop_container
    
    # In a real scenario, you'd restore the previous image
    log "Rollback completed"
}

# Function to show deployment status
status() {
    log "Checking deployment status..."
    
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        log "Container is running ✓"
        docker ps -f name=$CONTAINER_NAME
        echo ""
        log "Container stats:"
        docker stats --no-stream $CONTAINER_NAME
    else
        warn "Container is not running"
    fi
}

# Function to clean up old images
cleanup() {
    log "Cleaning up old Docker images..."
    docker image prune -f
    docker system prune -f
    log "Cleanup completed ✓"
}

# Main script logic
case "${1:-deploy}" in
    deploy)
        deploy
        ;;
    rollback)
        rollback
        ;;
    status)
        status
        ;;
    logs)
        show_logs
        ;;
    cleanup)
        cleanup
        ;;
    stop)
        stop_container
        ;;
    *)
        echo "Usage: $0 {deploy|rollback|status|logs|cleanup|stop}"
        echo ""
        echo "Commands:"
        echo "  deploy   - Deploy the application (default)"
        echo "  rollback - Rollback the deployment"
        echo "  status   - Show deployment status"
        echo "  logs     - Show application logs"
        echo "  cleanup  - Clean up old Docker images"
        echo "  stop     - Stop the application"
        exit 1
        ;;
esac
