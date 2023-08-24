# Market Data Ingestion and BigQuery Integration
![alt Application Cover](images/cover.jpg)



## Introduction

The Market Data Ingestion project focuses on fetching market data from a specified API and storing it in Google BigQuery. This project is designed to provide an automated solution for collecting and analyzing financial market data for further insights and analysis.

Key Aspects of the Project:

Data Ingestion: The project involves setting up a pipeline to fetch market data from a designated API source. This data includes information such as stock prices, trading volumes, and other relevant financial metrics.

Google BigQuery Integration: The collected market data is stored in Google BigQuery, a powerful cloud-based data warehouse. This integration allows for efficient storage, organization, and querying of large datasets.

Configuration Management: The project provides configuration files where API access credentials, BigQuery project details, and data loading settings can be customized based on specific requirements.

Automation: The project is designed to automate the data ingestion process. With the appropriate configuration, the system can fetch and load data periodically without manual intervention.

Data Analysis: While the project itself does not perform extensive data analysis, the stored data in BigQuery becomes accessible for advanced querying and analysis. Users can derive insights, trends, and patterns from the data.

Modularity: The project is structured with modularity in mind, making it easier to extend or adapt for different data sources, APIs, and analysis needs.

Usage: Users can execute the project scripts to initiate data ingestion and storage processes. This provides a streamlined approach for managing and handling financial market data.

Customization: The project's configuration files and scripts can be tailored to suit specific API endpoints, data formats, and BigQuery datasets.

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
3. Initialize all the environment variables 
    ```bash
    source gcp_project/init.sh
    ```
4. Build project:
    ```bash
    make build
    ```
This command install the required Python packages and create GCP ressources for project. 


### Usage
Update the `config/job.json` and `config/job.json` file with your API credentials and BigQuery configuration.

Run the data ingestion script:
```bash
make run-ingest symbol=<The name of the equity of your choice> 
```

This will fetch the market data from the API and ingest it into your specified BigQuery dataset.

You can now perform SQL queries on the ingested data using Google BigQuery.

```bash
make run-query
```


### Configuration
You need to configure the project by editing the files in the folder `config`. 

Here are the key fields for `config/api.json`:
- `api_key`: Your API key for accessing the market data API.
- `url`: The endpoint URL of the market data API.
- `datatype`: Type of file for the data. Choose between "csv" or "json".

Here are the key fields for `config/job.json`:

- `source_format`: Specifies the format of the source data being loaded. Set to "CSV" for comma-separated values format.
- `write_disposition`: Specifies the behavior when writing data to the destination table. Set to "WRITE_TRUNCATE" to overwrite existing data.
- `ignore_unknown_values`: Indicates whether to ignore rows with unknown values or fields not matching the schema. Set to `true` to skip unknown rows.
- `partitioning_type`: Specifies the type of partitioning to apply to the table. Set to "MONTH" for monthly partitioning.
- `partitioning_field`: Specifies the field used for partitioning the table. Set to "timestamp" to partition by the `timestamp` field.
- `skip_leading_rows`: Number of rows at the file beginning to skip during loading. Set to `1` to skip the header row.
- `schema`: Schema of the imported data


### Testing 

The test script execute one use case : load stock market data for 3 companies (IBM, GOOGLE, APPLE) and show their analysis

Before running test, ensure that you have built the project using installation commands . 

Next command runs the  use case described above:
```bash
make run-test
```

Exemple of the result : 

```bash
Analyse of the stock market
make    run-query
...
Sample of the data
Waiting on bqjob_r4658babf68260a66_0000018a296f5881_1 ... (0s) Current status: DONE   
+------------+--------+---------+--------+--------+--------------+--------+
| timestamp  |  open  |  high   |  low   | close  |    volume    | symbol |
+------------+--------+---------+--------+--------+--------------+--------+
| 2023-06-29 | 189.08 |  190.07 | 188.94 | 189.59 |  4.6347308E7 | aapl   |
| 2023-06-14 | 183.37 |  184.39 | 182.02 | 183.95 |  5.7462882E7 | aapl   |
...
| 2023-06-23 | 185.55 |  187.56 | 185.01 | 186.68 |  5.3116996E7 | aapl   |
+------------+--------+---------+--------+--------+--------------+--------+
Total nb of rows
Waiting on bqjob_r6d28808463a3c336_0000018a296f64cc_1 ... (0s) Current status: DONE   
+---------+
| nb_rows |
+---------+
|     300 |
+---------+
Market stock analysis
Waiting on bqjob_r49cd60bd6a753afa_0000018a296f7150_1 ... (0s) Current status: DONE   
+---------+-------------+---------------+-----------+------------------+------------------+
| company | latest_date | earliest_date | avg_close | price_change_pct | price_volatility |
+---------+-------------+---------------+-----------+------------------+------------------+
| goog    |  2023-08-24 |    2023-04-03 |    119.92 |             0.28 |             8.98 |
| aapl    |  2023-08-24 |    2023-04-03 |    178.98 |             0.23 |            10.14 |
| ibm     |  2023-08-24 |    2023-04-03 |    133.09 |             0.21 |             6.83 |
+---------+-------------+---------------+-----------+------------------+------------------+
```


Here are a few interpretations of the results:

* "Apple (AAPL)" has the highest average close of $178.98, which might indicate a relatively strong stock performance in terms of price.

* Among the three companies, "Google (GOOG)" has the highest price change percentage of 0.28%, suggesting the highest relative increase in stock price over the analyzed period.

* "IBM" has the lowest price volatility of 6.83%, indicating a relatively stable stock price movement compared to the other companies.


### Contributing
Contributions are welcome! If you have any ideas, improvements, or bug fixes, please feel free to open an issue or submit a pull request.

### License
This project is licensed under the MIT License.
