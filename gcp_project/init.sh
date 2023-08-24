PROJECT_ID=$(gcloud config get-value project)

BUCKET=${PROJECT_ID}-cf-staging
DATASET=data_ingest
REGION=us-central1

SERVICE_NAME=ingest-market-data
SERVICE_ACCOUNT_NAME=svc-market-ingest
SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

echo "SET ENVIRONMENT VARIABLES : "

export PROJECT_ID=$PROJECT_ID
export BUCKET_NAME=$BUCKET
export SERVICE_NAME=$SERVICE_NAME
export DATASET=$DATASET
export SERVICE_ACCOUNT_NAME=$SERVICE_ACCOUNT_NAME
export SERVICE_ACCOUNT_EMAIL=$SERVICE_ACCOUNT_EMAIL
export REGION=$REGION


env | grep  -E 'PROJECT_ID|REGION|BUCKET_NAME|SERVICE_NAME|DATASET|SERVICE_ACCOUNT_NAME|SERVICE_ACCOUNT_EMAIL'