# Mismatch Recruiter - Deployment Guide (Phase 5)

## 🚀 Deployment to Yandex Cloud

### Prerequisites
- Yandex Cloud account with active billing
- YC CLI installed (`yc` command available)
- Docker installed locally
- GitHub repository configured

### Step 1: Prepare Yandex Cloud Environment

```bash
# Login to Yandex Cloud
yc auth login

# Set default folder
export YC_FOLDER_ID="your-folder-id"
yc config set folder-id $YC_FOLDER_ID

# Create service account for deployment
yc iam service-account create --name mismatch-recruiter-sa

# Get service account ID
SERVICE_ACCOUNT_ID=$(yc iam service-account get --name mismatch-recruiter-sa --format=json | jq -r .id)

# Grant roles
yc resource-manager folder add-access-binding $YC_FOLDER_ID \\
  --role=container-registry.images.pusher \\
  --subject=serviceAccount:$SERVICE_ACCOUNT_ID
```

### Step 2: Create Docker Image

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "-m", "app.main"]
EOF

# Build image
docker build -t mismatch-recruiter:latest .
```

### Step 3: Push to Container Registry

```bash
# Configure Docker for Yandex Container Registry
echo $YC_OAUTH_TOKEN | docker login --username oauth --password-stdin cr.yandex

# Tag image
docker tag mismatch-recruiter:latest \\
  cr.yandex/$YC_FOLDER_ID/mismatch-recruiter:latest

# Push to registry
docker push cr.yandex/$YC_FOLDER_ID/mismatch-recruiter:latest
```

### Step 4: Deploy to Cloud Run

```bash
# Create Cloud Function or deploy to Cloud Run
yc serverless containers deploy mismatch-recruiter \\
  --image cr.yandex/$YC_FOLDER_ID/mismatch-recruiter:latest \\
  --memory 256mb \\
  --core-fraction 50 \\
  --execution-timeout 600s \\
  --environment DB_URL=sqlite:///app.db \\
  --environment FLASK_ENV=production
```

### Step 5: Set Up Database (PostgreSQL in Yandex Managed Service)

```bash
# Create PostgreSQL cluster
yc managed-postgresql cluster create mismatch-db \\
  --environment=PRESTABLE \\
  --network-name=default \\
  --host-class=b1.c1 \\
  --disk-size=10gb

# Create database
yc managed-postgresql database create mismatch_recruiter \\
  --cluster-name=mismatch-db

# Create user
yc managed-postgresql user create recruiter \\
  --cluster-name=mismatch-db \\
  --password=secure_password_here

# Get connection string
yc managed-postgresql cluster get mismatch-db --format=json | jq '.network_interfaces[0].primary_v4_address.address'
```

### Step 6: Configure Environment Variables

```bash
# In Yandex Cloud console or via CLI:
# Set these variables in your Cloud Function/Container environment:

FLASK_ENV=production
DATABASE_URL=postgresql://recruiter:password@host:5432/mismatch_recruiter
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
CORS_ORIGINS=https://your-frontend-domain.com
```

### Step 7: Set Up API Gateway

```bash
# Create API Gateway for Cloud Functions
yc serverless api-gateway create mismatch-api \\
  --spec=<(cat <<'SPEC'
apiVersion: serverless.yandex.cloud/v1
kind: ApiGateway
metadata:
  name: mismatch-api
spec:
  routes:
    - path: /api/{proxy+}
      x-yc-function:
        functionRef:
          name: mismatch-recruiter
SPEC
  )
```

### Step 8: Configure Custom Domain

```bash
# Create certificate in Certificate Manager
yc certificate-manager certificate request \\
  --name=mismatch-domain \\
  --domains=api.mismatch.recruiter

# Link certificate to API Gateway
yc serverless api-gateway update mismatch-api \\
  --certificate-id=your-cert-id
```

### Step 9: Health Check & Monitoring

```bash
# Test deployment
curl -X GET https://api.mismatch.recruiter/health

# Check logs
yc serverless container logs --name=mismatch-recruiter --limit=100

# Monitor performance
yc monitoring read --query='count()' \\
  --resource-type=container \\
  --labels service=mismatch-recruiter
```

### Step 10: Set Up CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Yandex Cloud

on:
  push:
    branches: [master]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t mismatch-recruiter:${{ github.sha }} .
      
      - name: Push to registry
        env:
          YC_REGISTRY_ID: ${{ secrets.YC_REGISTRY_ID }}
          YC_SA_KEY: ${{ secrets.YC_SA_KEY }}
        run: |
          echo $YC_SA_KEY | docker login --username json_key --password-stdin cr.yandex
          docker tag mismatch-recruiter:${{ github.sha }} cr.yandex/$YC_REGISTRY_ID/mismatch-recruiter:latest
          docker push cr.yandex/$YC_REGISTRY_ID/mismatch-recruiter:latest
      
      - name: Deploy to Cloud Run
        env:
          YC_FOLDER_ID: ${{ secrets.YC_FOLDER_ID }}
        run: |
          yc serverless containers deploy mismatch-recruiter \\
            --image cr.yandex/$YC_FOLDER_ID/mismatch-recruiter:latest
```

## 🔐 Security Checklist

- [☐] All secrets stored in Yandex Lockbox or GitHub Secrets
- [☐] Database has strong password
- [☐] CORS properly configured
- [☐] SSL/TLS certificates valid
- [☐] IAM roles follow least privilege principle
- [☐] API rate limiting configured
- [☐] Authentication enabled on all endpoints

## 📊 Monitoring & Alerts

```bash
# Create alert for high error rate
yc monitoring alert create mismatch-errors \\
  --notification-channel=your-channel-id \\
  --metric-name=errors_total \\
  --severity=critical \\
  --threshold=100
```

## 🔄 Rollback Procedure

```bash
# List previous versions
yc serverless container list

# Rollback to previous version
yc serverless container deploy mismatch-recruiter \\
  --image=cr.yandex/$YC_FOLDER_ID/mismatch-recruiter:previous-tag
```

## 🔗 Useful Links

- [Yandex Cloud Documentation](https://cloud.yandex.com/docs)
- [Cloud Functions Guide](https://cloud.yandex.com/docs/functions/)
- [Container Registry](https://cloud.yandex.com/docs/container-registry/)
- [PostgreSQL Managed Service](https://cloud.yandex.com/docs/managed-postgresql/)

