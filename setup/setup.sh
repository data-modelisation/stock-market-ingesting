#!/bin/bash

# Load variables from .env file
source .env

SVC_PRINCIPAL=serviceAccount:${SERVICE_ACCOUNT_EMAIL}

# Create bucket
gsutil ls gs://$BUCKET || gsutil mb -l $REGION gs://$BUCKET
echo "Bucket '$BUCKET' has been successfully created"
#  enable uniform bucket-level access on a bucket
# it enforces a more uniform and consistent access control model
gsutil uniformbucketlevelaccess set on gs://$BUCKET

# Create a new service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="market data ingest" \
    --description="description of the market data ingest"

# Add rights for account :

# - make the service account the admin of the bucket
# - it can read/write/list/delete etc. on only this bucket
gsutil iam ch ${SVC_PRINCIPAL}:roles/storage.admin gs://$BUCKET

# - ability to create/delete partitions etc in BigQuery table
bq --project_id=${PROJECT_ID} query --nouse_legacy_sql \
  "GRANT \`roles/bigquery.dataOwner\` ON $DATASET  TO '$SVC_PRINCIPAL' "

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member ${SVC_PRINCIPAL} \
  --role roles/bigquery.jobUser

# - make sure the sevice account can invoke cloud functions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member ${SVC_PRINCIPAL} \
  --role roles/run.invoker