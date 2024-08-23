#!/bin/bash

docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/gp2-release-terra/genotools/genotracker-fastapi -f Dockerfile.fastapi .
# docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/gp2-release-terra/genotools/genotracker-streamlit -f Dockerfile.streamlit .

docker push us-central1-docker.pkg.dev/gp2-release-terra/genotools/genotracker-fastapi
# docker push us-central1-docker.pkg.dev/gp2-release-terra/genotools/genotracker-streamlit

gcloud run deploy genotracker-fastapi \
  --image us-central1-docker.pkg.dev/gp2-release-terra/genotools/genotracker-fastapi \
  --platform managed \
  --region us-central1 \
  --service-account genotracker@gp2-release-terra.iam.gserviceaccount.com


gcloud app deploy

echo "Deployment complete."