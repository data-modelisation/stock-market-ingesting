# Market Data Ingestion and BigQuery Integration

Welcome to the Market Data Ingestion and BigQuery Integration project! 
This project aims to fetch market data from an API and then store it in Google BigQuery for further analysis and processing.

## Introduction

In this project, developed soulution fetches market data from a specified API and stores it into a Google BigQuery dataset. 
This allows for easy analysis and querying of the market data using SQL.

## Getting Started

### Prerequisites

Before you begin, make sure you have the following:

- Python 3.x installed
- Google Cloud Platform account with BigQuery access
- [API access credentials](https://www.alphavantage.co/support/#api-key)  for the market data source

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/market-data-ingestion.git
   ```
2. Navigate to the project directory:

    ```bash
    cd market-data-ingestion
    ```
3. Install the required Python packages using pip:
    ```bash
    make intall
    ```

4. Put current configuration  file .env 
    ```bash
    make init
    ```

5. Create bucket and service account as indicated in .env
    ```bash
    make setup
    ```


### Usage
Update the `config/job.json` and `config/job.json` file with your API credentials and BigQuery configuration.

Run the data ingestion script:
```bash
make run-ingest symbol=<The name of the equity of your choice> 
```

This will fetch the market data from the API and ingest it into your specified BigQuery dataset.

You can now perform SQL queries on the ingested data using Google BigQuery.


### Configuration
You need to configure the project by editing the files in the folder `config`. 

Here are the key fields for `config/api.json`:
```bash
api_key: Your API key for accessing the market data API.
url: The endpoint URL of the market data API.
datatype: Type of file : csv or json 
```

Here are the key fields for `config/job.json`:
```bash
bigquery_project_id: Your Google Cloud project ID.
bigquery_dataset: The name of the BigQuery dataset where the data will be stored.
bigquery_table: The name of the BigQuery table where the data will be stored.
```

### Contributing
Contributions are welcome! If you have any ideas, improvements, or bug fixes, please feel free to open an issue or submit a pull request.

### License
This project is licensed under the MIT License.
