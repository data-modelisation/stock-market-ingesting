import os
import logging
from flask import Flask
from flask import request, escape
from ingest import ingest
from cloud import upload


app = Flask(__name__)

@app.route("/", methods=['POST'])
def ingest_data():
    try:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        json = request.get_json(force=True) # https://stackoverflow.com/questions/53216177/http-triggering-cloud-function-with-cloud-scheduler/60615210#60615210

        api_url = "https://api.example.com/data"
        symbol = escape(json['symbol'])  # required
        bucket = escape(json['bucket'])  # required
        tableref, numrows = ingest(symbol, bucket)
        ok = 'Success ... ingested {} rows to {}'.format(numrows, tableref)
        logging.info(ok)
        return 'Success'
    except Exception as e:
        logging.exception("Failed to ingest ... try again later?")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")