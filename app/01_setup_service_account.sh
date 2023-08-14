#!/bin/bash
SERVICE_ACCOUNT_NAME=svc-market-ingest
PROJECT_ID=$(gcloud config get-value project)
REGION=us-central1
SVC_PRINCIPAL=serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

# create bucket
gsutil ls gs://$BUCKET || gsutil mb -l $REGION gs://$BUCKET
#  enable uniform bucket-level access on a bucket
# it enforces a more uniform and consistent access control model
gsutil uniformbucketlevelaccess set on gs://$BUCKET


# create a new service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name "market data ingest" \
    --description "description of the market data ingest"