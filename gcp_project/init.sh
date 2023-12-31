PROJECT_ID=$(gcloud config get-value project)

BUCKET=${PROJECT_ID}-cf-staging
REGION=us-central1

DATASET=data_ingest
SERVICE_NAME=ingest-market-data
SERVICE_ACCOUNT_NAME=svc-market-ingest
SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

export PROJECT_ID=$PROJECT_ID
export REGION=$REGION
export BUCKET_NAME=$BUCKET
export SERVICE_NAME=$SERVICE_NAME
export DATASET=$DATASET
export SERVICE_ACCOUNT_NAME=$SERVICE_ACCOUNT_NAME
export SERVICE_ACCOUNT_EMAIL=$SERVICE_ACCOUNT_EMAIL


