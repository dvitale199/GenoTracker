#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <PROJECT_ID> <REGION> <SERVICE_ACCOUNT>"
  exit 1
fi

PROJECT_ID="$1"
REGION="$2"
SERVICE_ACCOUNT="$3"

# gcloud auth login
# gcloud config set project $PROJECT_ID

docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/$PROJECT_ID/genotools/genotracker-fastapi -f Dockerfile.fastapi .
docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/$PROJECT_ID/genotools/genotracker-streamlit -f Dockerfile.streamlit .

docker push us-central1-docker.pkg.dev/$PROJECT_ID/genotools/genotracker-fastapi
docker push us-central1-docker.pkg.dev/$PROJECT_ID/genotools/genotracker-streamlit

gcloud run deploy genotracker-fastapi \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/genotools/genotracker-fastapi \
  --platform managed \
  --region $REGION \
  --service-account $SERVICE_ACCOUNT

FASTAPI_URL=$(gcloud run services describe genotracker-fastapi --platform managed --region $REGION --format 'value(status.url)')

echo "Waiting for FastAPI service to be ready..."
until $(curl --output /dev/null --silent --head --fail "$FASTAPI_URL/health"); do
  printf '.'
  sleep 5
done

gcloud run deploy genotracker-streamlit \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/genotools/genotracker-streamlit \
  --platform managed \
  --region $REGION \
  --service-account $SERVICE_ACCOUNT

echo "Deployment complete."