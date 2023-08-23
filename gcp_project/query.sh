#!/bin/bash
# Exit immediately if any command fails
set -o errexit

# Load variables from .env file
source .env

# Construct the SQL query
query="SELECT * FROM \`${PROJECT_ID}.${DATASET}.market_data_raw*\` LIMIT 10;"

# Print the SQL query (optional)
echo "Running query : $query"

# Run the BigQuery query
bq query --nouse_legacy_sql "$query"

# Construct the SQL query
query="SELECT COUNT(*) as nb_rows FROM \`${PROJECT_ID}.${DATASET}.market_data_raw*\`;"

# Print the SQL query (optional)
echo "Running query : $query"

# Run the BigQuery query
bq query --nouse_legacy_sql "$query"