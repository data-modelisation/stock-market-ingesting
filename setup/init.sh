PROJECT_ID=$(gcloud config get-value project)

BUCKET=${PROJECT_ID}-cf-staging
DATASET=data_ingest
REGION=us-central1

SERVICE_NAME=ingest-market-data
SERVICE_ACCOUNT_NAME=svc-market-ingest
SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
#SVC_PRINCIPAL=serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

# Create or overwrite the config.env file with the configuration
echo "PROJECT_ID=$PROJECT_ID" >> .env
echo "BUCKET_NAME=$BUCKET" >> .env
echo "SERVICE_NAME=$SERVICE_NAME" >> .env
echo "DATASET=$DATASET" >> .env
echo "SERVICE_ACCOUNT_NAME=$SERVICE_ACCOUNT_NAME" >> .env
echo "SERVICE_ACCOUNT_EMAIL=$SERVICE_ACCOUNT_EMAIL" >> .env