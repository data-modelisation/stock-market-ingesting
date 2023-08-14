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
- API access credentials  for the market data source

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
    pip install -r requirements.txt
    ```

...

### Usage
Update the config.json file with your API credentials and BigQuery configuration.

Run the data ingestion script:
```bash
python ingest_data.py
```

This will fetch the market data from the API and ingest it into your specified BigQuery dataset.

You can now perform SQL queries on the ingested data using Google BigQuery.

### Configuration
You need to configure the project by editing the config.json file. Here are the key fields:
```bash
api_key: Your API key for accessing the market data API.
api_endpoint: The endpoint URL of the market data API.
bigquery_project_id: Your Google Cloud project ID.
bigquery_dataset: The name of the BigQuery dataset where the data will be stored.
bigquery_table: The name of the BigQuery table where the data will be stored.
```

### Contributing
Contributions are welcome! If you have any ideas, improvements, or bug fixes, please feel free to open an issue or submit a pull request.

### License
This project is licensed under the MIT License.
