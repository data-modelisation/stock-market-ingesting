import os
import gzip
import shutil
import logging
import os.path
from urllib.request import urlopen
import zipfile
import datetime
import tempfile
import csv
from google.cloud import storage
from google.cloud.storage import Blob
from google.cloud import bigquery
import json
from urllib.parse import urlencode, urlunparse
import sys

"""
 Retrieve and construct a BigQuery confiration file.
 Return: A configured LoadJobConfig object for data loading.
"""
def get_bq_load_config():
    with open('config/job.json') as config_file: 
        config = json.load(config_file)    

    load_config = bigquery.LoadJobConfig()
    load_config.source_format = config['source_format']
    load_config.write_disposition = config['write_disposition']
    load_config.ignore_unknown_values = config['ignore_unknown_values']
    load_config.time_partitioning = bigquery.table.TimePartitioning(config['partitioning_type'], config['partitioning_field'])
    load_config.skip_leading_rows = config['skip_leading_rows']
    load_config.schema = [
        bigquery.SchemaField(field['name'], field['type']) for field in config['schema']
    ]

    return load_config

    
def bqload(gcsfile, symbol):
    """
    Loads the CSV file in GCS into BigQuery, replacing the existing data in that partition
    """
    load_config = get_bq_load_config()
    client = bigquery.Client.from_service_account_json("config/account.json")
    #client = bigquery.Client()

    table_ref = client.dataset(os.environ.get("DATASET")).table('market_data_raw_{}'.format(symbol))
   
    load_job = client.load_table_from_uri(gcsfile, table_ref, job_config=load_config)
    load_job.result()  # waits for table load to complete

    if load_job.state != 'DONE':
        raise load_job.exception()

    return table_ref, load_job.output_rows


def upload(csvfile, blobname):
    """
    Uploads the CSV file into the bucket with the given blobname
    """
    bucketname = os.environ.get("BUCKET_NAME")
    
    client = storage.Client()
    bucket = client.get_bucket(bucketname)
    logging.info(bucket)
    logging.debug('Uploading {} ...'.format(csvfile))

    blob = Blob(blobname, bucket)
    blob.upload_from_filename(csvfile)
    gcslocation = 'gs://{}/{}'.format(bucketname, blobname)

    logging.info('Uploaded {} ...'.format(gcslocation))

    return gcslocation

def get_config(path: str):
    with open(path) as config_file:
        config = json.load(config_file)
    return config

def download(symbol: str, destdir: str):
    """
    Downloads the market stock data and returns local filename
    """
    logging.info('Requesting data for {}-*'.format(symbol))

    config = get_config('config/api.json')

    query_params = {
        "apikey": config['apikey'],
        "datatype": config['datatype'],
        "symbol" : symbol
    }

    url = config['url'] + '&'+urlencode(query_params)

    logging.debug("Trying to download {}".format(url))

    input_filename = os.path.join(destdir, "input_{}".format(symbol))
    output_filename = os.path.join(destdir, "{}".format(symbol))
    
    with open(input_filename, "wb") as fp:
        response = urlopen(url)
        fp.write(response.read())

    # Add column symbol 
    # Add the "symbol" value to each row
    with open(input_filename, "r") as input_file, open(output_filename, "w", newline="") as output_file:
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        # Write the modified header
        header = next(csv_reader)
        header.append("symbol")
        csv_writer.writerow(header)

        # Write the modified rows
        for row in csv_reader:
            row.append(symbol)
            csv_writer.writerow(row)

    logging.debug("{} saved".format(output_filename))

    return os.path.join(destdir,output_filename)

def ingest(symbol):
    '''
   Ingest stock market data from API to Google Cloud Storage
   return table, numrows on success.
   '''
    tempdir = tempfile.mkdtemp(prefix='ingest_market_data')
    try:
        tempdir = tempfile.mkdtemp(prefix='ingest_market_data')
        data_csv = download(symbol, tempdir)
        gcsloc = 'data_market/raw/market_data_{}.csv'.format(symbol)
        gcsloc = upload(data_csv, gcsloc)

        return bqload(gcsloc, symbol)
    finally:
        logging.debug('Cleaning up by removing {}'.format(tempdir))
        shutil.rmtree(tempdir)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Ingest data from API to Google Cloud Storage')
    parser.add_argument('--symbol', help='Name of market item', required=True)
    parser.add_argument('--debug', dest='debug', action='store_true', help='Specify if you want debug messages')

    try:
        args = parser.parse_args()
        if args.debug:
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

        tableref, numrows = ingest(args.symbol)

        #logging.info('Success ... ingested {} rows to {}'.format(numrows, tableref))
    except Exception as e:
        logging.exception("Try again later?")