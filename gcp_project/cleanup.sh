#!/bin/bash

# Exit immediately if any command fails
set -o errexit

source  gcp_project/init.sh
# Delete all elements

# Remove the binding for service account from Cloud Functions invoker role
gcloud projects remove-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role roles/run.invoker

# Remove the binding for service account from BigQuery roles
gcloud projects remove-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role roles/bigquery.dataOwner

gcloud projects remove-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role roles/bigquery.jobUser

# Remove rights for service account from the bucket
gsutil iam ch -d serviceAccount:${SERVICE_ACCOUNT_EMAIL}:roles/storage.admin gs://$BUCKET_NAME

# Delete the service account
gcloud iam service-accounts delete $SERVICE_ACCOUNT_EMAIL --quiet

# Delete the bucket and its contents
gsutil -m rm -r gs://$BUCKET_NAME

echo "All elements have been successfully deleted"
