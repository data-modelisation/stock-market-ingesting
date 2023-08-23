source .env

bq query --nouse_legacy_sql \  
"SELECT  
    COUNT(*)  
FROM  
   \`${PROJECT_ID}.${DATASET}.*\`;"

