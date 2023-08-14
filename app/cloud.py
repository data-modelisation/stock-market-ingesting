
import os
import gzip
import shutil
import logging
import os.path
import zipfile
import datetime
import tempfile
from google.cloud import storage
from google.cloud.storage import Blob
from google.cloud import bigquery

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


# def bqload(gcsfile, year, month):
#     """
#     Loads the CSV file into BigQuery 
#     Replacing the existing data in that partition
#     """
#     client = bigquery.Client()
#     # truncate existing partition ...
#     table_ref = client.dataset('dsongcp').table('flights_raw${}{}'.format(year, month))
#     job_config = bigquery.LoadJobConfig()
#     job_config.source_format = 'CSV'
#     job_config.write_disposition = 'WRITE_TRUNCATE'
#     job_config.ignore_unknown_values = True
#     job_config.time_partitioning = bigquery.table.TimePartitioning('MONTH', 'FlightDate')
#     job_config.skip_leading_rows = 1
#     job_config.schema = [
#         bigquery.SchemaField(col_and_type.split(':')[0], col_and_type.split(':')[1])  #, mode='required')
#         for col_and_type in
#         "Year:STRING,Quarter:STRING,Month:STRING,DayofMonth:STRING,DayOfWeek:STRING,FlightDate:DATE,Reporting_Airline:STRING,DOT_ID_Reporting_Airline:STRING,IATA_CODE_Reporting_Airline:STRING,Tail_Number:STRING,Flight_Number_Reporting_Airline:STRING,OriginAirportID:STRING,OriginAirportSeqID:STRING,OriginCityMarketID:STRING,Origin:STRING,OriginCityName:STRING,OriginState:STRING,OriginStateFips:STRING,OriginStateName:STRING,OriginWac:STRING,DestAirportID:STRING,DestAirportSeqID:STRING,DestCityMarketID:STRING,Dest:STRING,DestCityName:STRING,DestState:STRING,DestStateFips:STRING,DestStateName:STRING,DestWac:STRING,CRSDepTime:STRING,DepTime:STRING,DepDelay:STRING,DepDelayMinutes:STRING,DepDel15:STRING,DepartureDelayGroups:STRING,DepTimeBlk:STRING,TaxiOut:STRING,WheelsOff:STRING,WheelsOn:STRING,TaxiIn:STRING,CRSArrTime:STRING,ArrTime:STRING,ArrDelay:STRING,ArrDelayMinutes:STRING,ArrDel15:STRING,ArrivalDelayGroups:STRING,ArrTimeBlk:STRING,Cancelled:STRING,CancellationCode:STRING,Diverted:STRING,CRSElapsedTime:STRING,ActualElapsedTime:STRING,AirTime:STRING,Flights:STRING,Distance:STRING,DistanceGroup:STRING,CarrierDelay:STRING,WeatherDelay:STRING,NASDelay:STRING,SecurityDelay:STRING,LateAircraftDelay:STRING,FirstDepTime:STRING,TotalAddGTime:STRING,LongestAddGTime:STRING,DivAirportLandings:STRING,DivReachedDest:STRING,DivActualElapsedTime:STRING,DivArrDelay:STRING,DivDistance:STRING,Div1Airport:STRING,Div1AirportID:STRING,Div1AirportSeqID:STRING,Div1WheelsOn:STRING,Div1TotalGTime:STRING,Div1LongestGTime:STRING,Div1WheelsOff:STRING,Div1TailNum:STRING,Div2Airport:STRING,Div2AirportID:STRING,Div2AirportSeqID:STRING,Div2WheelsOn:STRING,Div2TotalGTime:STRING,Div2LongestGTime:STRING,Div2WheelsOff:STRING,Div2TailNum:STRING,Div3Airport:STRING,Div3AirportID:STRING,Div3AirportSeqID:STRING,Div3WheelsOn:STRING,Div3TotalGTime:STRING,Div3LongestGTime:STRING,Div3WheelsOff:STRING,Div3TailNum:STRING,Div4Airport:STRING,Div4AirportID:STRING,Div4AirportSeqID:STRING,Div4WheelsOn:STRING,Div4TotalGTime:STRING,Div4LongestGTime:STRING,Div4WheelsOff:STRING,Div4TailNum:STRING,Div5Airport:STRING,Div5AirportID:STRING,Div5AirportSeqID:STRING,Div5WheelsOn:STRING,Div5TotalGTime:STRING,Div5LongestGTime:STRING,Div5WheelsOff:STRING,Div5TailNum:STRING".split(',')
#     ]
#     load_job = client.load_table_from_uri(gcsfile, table_ref, job_config=job_config)
#     load_job.result()  # waits for table load to complete

#     if load_job.state != 'DONE':
#         raise load_job.exception()

#     return table_ref, load_job.output_rows