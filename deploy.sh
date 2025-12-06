#!/bin/bash
# Deploy script for Yandex Cloud Functions

FUNCTION_NAME="recruitment-ai-function"
FOLDER_ID="b1gl37qg99ijsedu73rh"
SERVICE_ACCOUNT_ID="ajemrh6g4t61hl67eq73"

# Create function
yc serverless function create \
  --name \recruitment-ai-function \
  --folder-id \b1gl37qg99ijsedu73rh

# Create version with code
yc serverless function version create \
  --function-name \recruitment-ai-function \
  --runtime python311 \
  --entrypoint main.recruitment_handler \
  --memory 512MB \
  --execution-timeout 30s \
  --service-account-id \ \
  --environment YANDEX_API_KEY=AQVNzKCGqn7mm3lfQ0T5JoWx8J4FP0TIVoA9i1o \
  --environment FOLDER_ID=b1gl37qg99ijsedu73rh \
  --environment TELEGRAM_BOT_TOKEN=8251890606:AAErf71pVupIo9TVsdS1acuW-Drn6KuYПгk \
  --source-path .

# Create trigger
yc serverless trigger create timer \
  --name recruitment-ai-timer \
  --cron-expression '0 * * * ?' \
  --function-name \recruitment-ai-function \
  --function-service-account-id \

echo "Deployment completed!"
