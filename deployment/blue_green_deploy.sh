deployment/blue_green_deploy.sh#!/bin/bash

# Blue-Green Deployment Strategy
# This script manages zero-downtime deployments using Blue-Green pattern
# Maintains two identical production environments (Blue and Green)
# Traffic switches between them during deployment

set -e

LOG_FILE="/var/log/deployment.log"
BLUE_PORT=5001
GREEN_PORT=5002
LOAD_BALANCER_CONFIG="/etc/nginx/sites-enabled/app.conf"
GIT_REPO="/app/repo"
APP_DIR_BLUE="/app/blue"
APP_DIR_GREEN="/app/green"

# Color output
RED='\033[0;31m'
GREEN_COLOR='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN_COLOR}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Determine current active environment
get_active_env() {
    if grep -q "server localhost:$BLUE_PORT" "$LOAD_BALANCER_CONFIG"; then
        echo "blue"
    else
        echo "green"
    fi
}

# Get inactive environment
get_inactive_env() {
    if [ "$(get_active_env)" = "blue" ]; then
        echo "green"
    else
        echo "blue"
    fi
}

# Health check function
health_check() {
    local port=$1
    local max_retries=30
    local retry=0

    while [ $retry -lt $max_retries ]; do
        if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
            log_info "Health check passed for port $port"
            return 0
        fi
        log_warning "Health check failed, retrying... ($((retry + 1))/$max_retries)"
        sleep 2
        retry=$((retry + 1))
    done

    log_error "Health check failed after $max_retries retries"
    return 1
}

# Deploy to inactive environment
deploy_to_env() {
    local env=$1
    local app_dir
    local port

    if [ "$env" = "blue" ]; then
        app_dir="$APP_DIR_BLUE"
        port=$BLUE_PORT
    else
        app_dir="$APP_DIR_GREEN"
        port=$GREEN_PORT
    fi

    log_info "Deploying to $env environment (port: $port)"

    # Clone/update repository
    if [ -d "$app_dir" ]; then
        log_info "Updating existing $env deployment"
        cd "$app_dir"
        git pull origin master
    else
        log_info "Creating new $env deployment"
        mkdir -p "$app_dir"
        cd "$app_dir"
        git clone "$GIT_REPO" .
    fi

    # Install dependencies
    log_info "Installing dependencies for $env"
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Run database migrations
    log_info "Running database migrations for $env"
    flask db upgrade

    # Start application
    log_info "Starting $env application on port $port"
    export FLASK_ENV=production
    export PORT=$port
    gunicorn --workers 4 --worker-class gevent --bind 0.0.0.0:$port app:app > "${app_dir}/app.log" 2>&1 &
    echo $! > "${app_dir}/app.pid"

    # Health check
    if ! health_check $port; then
        log_error "Deployment to $env failed health check"
        kill_env $env
        return 1
    fi

    log_info "Successfully deployed to $env environment"
    return 0
}

# Switch traffic to environment
switch_traffic() {
    local target_env=$1
    local target_port

    if [ "$target_env" = "blue" ]; then
        target_port=$BLUE_PORT
    else
        target_port=$GREEN_PORT
    fi

    log_info "Switching traffic to $target_env (port: $target_port)"

    # Update nginx configuration
    sed -i "s/server localhost:[0-9]*/server localhost:$target_port/g" "$LOAD_BALANCER_CONFIG"

    # Reload nginx
    nginx -s reload

    log_info "Traffic successfully switched to $target_env"
}

# Kill application in environment
kill_env() {
    local env=$1
    local app_dir

    if [ "$env" = "blue" ]; then
        app_dir="$APP_DIR_BLUE"
    else
        app_dir="$APP_DIR_GREEN"
    fi

    if [ -f "${app_dir}/app.pid" ]; then
        local pid=$(cat "${app_dir}/app.pid")
        log_info "Killing $env application (PID: $pid)"
        kill $pid || true
        rm "${app_dir}/app.pid"
    fi
}

# Rollback to previous environment
rollback() {
    local current_env=$(get_active_env)
    log_warning "Rolling back to $current_env environment"

    local previous_env=$(get_inactive_env)
    log_info "Stopping failed deployment on $previous_env"
    kill_env $previous_env

    log_info "Rollback complete, traffic remains on $current_env"
}

# Main deployment process
main() {
    log_info "Starting Blue-Green deployment"

    local inactive_env=$(get_inactive_env)
    log_info "Current active environment: $(get_active_env)"
    log_info "Will deploy to: $inactive_env"

    # Deploy to inactive environment
    if ! deploy_to_env $inactive_env; then
        log_error "Deployment failed"
        rollback
        exit 1
    fi

    # Switch traffic
    if ! switch_traffic $inactive_env; then
        log_error "Traffic switch failed"
        rollback
        exit 1
    fi

    # Kill old environment
    local old_env=$(get_inactive_env)
    sleep 10 # Grace period for connection draining
    log_info "Stopping old $old_env environment"
    kill_env $old_env

    log_info "Blue-Green deployment completed successfully"
}

main "$@"
