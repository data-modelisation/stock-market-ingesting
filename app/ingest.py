import os
import gzip
import shutil
import logging
import os.path
from urllib.request import urlopen
import zipfile
import datetime
import tempfile
from google.cloud import storage
from google.cloud.storage import Blob
from google.cloud import bigquery

DATA_URL ="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=demo&datatype=csv"


def bqload(gcsfile, symbol):
    """
    Loads the CSV file in GCS into BigQuery, replacing the existing data in that partition
    """
    client = bigquery.Client()
    # truncate existing partition ...
    table_ref = client.dataset('data_ingest').table('market_data_raw${}{}'.format(symbol))
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = 'CSV'
    job_config.write_disposition = 'WRITE_TRUNCATE'
    job_config.ignore_unknown_values = True
    job_config.time_partitioning = bigquery.table.TimePartitioning('MONTH', 'FlightDate')
    job_config.skip_leading_rows = 1
    job_config.schema = [
        bigquery.SchemaField("timestamp",   "TIMESTAMP"),
        bigquery.SchemaField("open",        "FLOAT"),
        bigquery.SchemaField("high",        "FLOAT"),
        bigquery.SchemaField("low",         "FLOAT"),
        bigquery.SchemaField("close",       "FLOAT")
    ]
    load_job = client.load_table_from_uri(gcsfile, table_ref, job_config=job_config)
    load_job.result()  # waits for table load to complete

    if load_job.state != 'DONE':
        raise load_job.exception()

    return table_ref, load_job.output_rows


def upload(csvfile, bucketname, blobname):
    """
    Uploads the CSV file into the bucket with the given blobname
    """
    client = storage.Client()
    bucket = client.get_bucket(bucketname)
    logging.info(bucket)
    blob = Blob(blobname, bucket)
    logging.debug('Uploading {} ...'.format(csvfile))
    blob.upload_from_filename(csvfile)
    gcslocation = 'gs://{}/{}'.format(bucketname, blobname)
    logging.info('Uploaded {} ...'.format(gcslocation))

    return gcslocation

def download(symbol: str, destdir: str):
    """
    Downloads on-time performance data and returns local filename
    year e.g.'2015'
    month e.g. '01 for January
    """
    logging.info('Requesting data for {}-*'.format(symbol))
    url = os.path.join(DATA_URL,"&symbol={}".format(symbol))
    logging.debug("Trying to download {}".format(url))

    filename = os.path.join(destdir, "{}".format(symbol))
    with open(filename, "wb") as fp:
        response = urlopen(url)
        fp.write(response.read())
    logging.debug("{} saved".format(filename))
    return filename

def ingest(symbol, bucket):
    '''
   ingest flights data from BTS website to Google Cloud Storage
   return table, numrows on success.
   raises exception if this data is not on BTS website
   '''
    tempdir = tempfile.mkdtemp(prefix='ingest_flights')
    try:
        tempdir = tempfile.mkdtemp(prefix='ingest_market_data')
        symbol = "IBM"
        data_csv = download("IBM", tempdir)
        gcsloc = 'data_market/raw/{}.csv'.format(symbol)
        gcsloc = upload(data_csv, bucket, gcsloc)

        return bqload(gcsloc, symbol)
    finally:
        logging.debug('Cleaning up by removing {}'.format(tempdir))
        shutil.rmtree(tempdir)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='ingest data from API to Google Cloud Storage')
    parser.add_argument('--bucket', help='GCS bucket to upload data to', required=True)
    parser.add_argument('--debug', dest='debug', action='store_true', help='Specify if you want debug messages')

    try:
        args = parser.parse_args()
        if args.debug:
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

        tableref, numrows = ingest(args.bucket)
        logging.info('Success ... ingested {} rows to {}'.format(numrows, tableref))
    except Exception as e:
        logging.exception("Try again later?")