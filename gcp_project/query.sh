#!/bin/bash
# Exit immediately if any command fails
set -o errexit

# Construct the SQL query
query="SELECT * FROM \`${PROJECT_ID}.${DATASET}.market_data_raw*\` LIMIT 10;"

# Print the SQL query (optional)
echo "Sample of the data"

# Run the BigQuery query
bq query --nouse_legacy_sql "$query"

# Construct the SQL query
query="SELECT COUNT(*) as nb_rows FROM \`${PROJECT_ID}.${DATASET}.market_data_raw*\`;"

# Print the SQL query (optional)
echo "Total nb of rows"

# Run the BigQuery query
bq query --nouse_legacy_sql "$query"

# Print the SQL query (optional)
echo "Market stock analysis"

query="
WITH stock_performance AS (
  SELECT
    symbol AS company,
    MAX(timestamp) AS latest_date,
    MIN(timestamp) AS earliest_date,
    AVG(close) AS avg_close,
    (MAX(close) - MIN(close)) / MIN(close) AS price_change_pct,
    STDDEV_SAMP(close) AS price_volatility
  FROM \`${PROJECT_ID}.${DATASET}.market_data_raw*\` 
  GROUP BY
    company
)
SELECT
  company,
  latest_date,
  earliest_date,
  ROUND(avg_close, 2) as avg_close,
  ROUND(price_change_pct,2) as price_change_pct,
  ROUND(price_volatility,2) as price_volatility
FROM
  stock_performance
ORDER BY
  price_change_pct DESC;"

# Run the BigQuery query
bq query --nouse_legacy_sql "$query"