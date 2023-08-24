#!/bin/bash

# Exit immediately if any command fails
set -o errexit

source  gcp_project/init.sh 
# Create bucket
gsutil ls gs://${BUCKET_NAME} || gsutil mb -l $REGION gs://${BUCKET_NAME}
echo "Bucket '${BUCKET_NAME}' has been successfully created"
#  enable uniform bucket-level access on a bucket
# it enforces a more uniform and consistent access control model
gsutil uniformbucketlevelaccess set on gs://$BUCKET_NAME

# Create a new service account
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
    --display-name="market data ingest" \
    --description="description of the market data ingest"

# Add rights for account :
# - make the service account the admin of the bucket
# - it can read/write/list/delete etc. on only this bucket
gsutil iam ch serviceAccount:${SERVICE_ACCOUNT_EMAIL}:roles/storage.admin gs://${BUCKET_NAME}

# - ability to create/delete partitions etc in BigQuery table
# bq --project_id=${PROJECT_ID} query --nouse_legacy_sql \
#   "GRANT \`roles/bigquery.dataOwner\` ON $DATASET  TO '$SVC_PRINCIPAL' "
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role roles/bigquery.dataOwner

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role roles/bigquery.jobUser

# Generate credentials for service account
gcloud iam service-accounts keys create ./config/account.json \
  --iam-account=${SERVICE_ACCOUNT_EMAIL}
