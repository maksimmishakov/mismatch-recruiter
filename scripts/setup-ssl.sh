#!/bin/bash
# Setup SSL certificates using Let's Encrypt

ENVIRONMENT=${1:-staging}

if [ "$ENVIRONMENT" = "staging" ]; then
  DOMAIN="staging-api.mismatch-recruiter.ru"
  APP_DOMAIN="staging.mismatch-recruiter.ru"
elif [ "$ENVIRONMENT" = "production" ]; then
  DOMAIN="api.mismatch-recruiter.ru"
  APP_DOMAIN="app.mismatch-recruiter.ru"
else
  echo "Usage: $0 staging|production"
  exit 1
fi

echo "Setting up SSL certificates for $DOMAIN"

# Install certbot if not present
if ! command -v certbot &> /dev/null; then
  echo "Installing certbot..."
  sudo apt-get update
  sudo apt-get install -y certbot python3-certbot-nginx
fi

# Create certificate
echo "Creating certificate for $DOMAIN..."
sudo certbot certonly --non-interactive --agree-tos --email admin@mismatch-recruiter.ru --dns-cloudflare -d $DOMAIN -d $APP_DOMAIN

echo "SSL certificates configured successfully!"
