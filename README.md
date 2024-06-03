# SEMTUI Pipeline Project

## Overview

This project is designed to automate data processing, reconciliation, and extension using the SEMTUI framework. The pipeline consists of three main steps:
1. **Loading and Modifying Data**
2. **Reconciling Data**
3. **Extending Data**

The pipeline is orchestrated using Docker Compose to ensure each step is executed in the correct order.

## Prerequisites

- Docker and Docker Compose installed on your machine
- Python 3.x installed
- Internet connection for fetching dependencies

## Directory Structure

Create the following directory structure to store the necessary files and outputs:

```sh
mkdir -p /path/to/your/project/pipeline_results/shared_data
mkdir -p /path/to/your/project/pipeline_results/csv_output_dir
mkdir -p /path/to/your/project/pipeline_results/completion_data
```

## .env File

Create a `.env` file in the root directory of your project with the following content. This file will contain all the necessary environment variables:

```env
API_URL=http://your.api.url/api/
USERNAME=your_username
PASSWORD=your_password
DATASET_ID=your_dataset_id
TABLE_NAME=your_table_name
COLUMN_NAME=City
ID_RECONCILIATOR=geocodingHere
RECONCILIATED_COLUMN_NAME=City
PROPERTIES=apparent_temperature_max,apparent_temperature_min,precipitation_sum
NEW_COLUMNS_NAME=Apparent_Max_Temperature,Apparent_Min_Temperature,Total_Precipitation
DATE_COLUMN_NAME=Fecha_id
ID_EXTENDER=meteoPropertiesOpenMeteo
WEATHER_PARAMS=apparent_temperature_max,apparent_temperature_min,precipitation_sum
OUTPUT_PATH_SHARED=/app/shared/processed_data.json
OUTPUT_PATH_CSV=/app/csv_output_dir/extended_data.csv
CSV_FILE_PATH=/app/csv_dir/your_input_file.csv
LOCAL_SHARED_DATA_PATH=/path/to/your/project/pipeline_results/shared_data
LOCAL_CSV_OUTPUT_DIR_PATH=/path/to/your/project/pipeline_results/csv_output_dir
LOCAL_COMPLETION_DATA_PATH=/path/to/your/project/pipeline_results/completion_data
```

## Docker Compose Configuration

Create a `docker-compose.yml` file in the root directory of your project with the following content:

```yaml
version: '3.8'
services:
  load_and_modify:
    build: ./load_and_modify
    volumes:
      - ${LOCAL_SHARED_DATA_PATH}:/app/shared
      - ${LOCAL_COMPLETION_DATA_PATH}:/app/completion
      - ${CSV_FILE_PATH}:/app/csv_dir
    environment:
      - API_URL=${API_URL}
      - USERNAME=${USERNAME}
      - PASSWORD=${PASSWORD}
      - OUTPUT_PATH=${OUTPUT_PATH_SHARED}
      - CSV_FILE_PATH=${CSV_FILE_PATH}

  reconciliation:
    build: ./reconciliation
    depends_on:
      - load_and_modify
    volumes:
      - ${LOCAL_SHARED_DATA_PATH}:/app/shared
      - ${LOCAL_COMPLETION_DATA_PATH}:/app/completion
    environment:
      - API_URL=${API_URL}
      - USERNAME=${USERNAME}
      - PASSWORD=${PASSWORD}
      - DATASET_ID=${DATASET_ID}
      - TABLE_NAME=${TABLE_NAME}
      - OUTPUT_PATH=${OUTPUT_PATH_SHARED}
    entrypoint: ["sh", "-c", "while [ ! -f /app/completion/load_and_modify_done ]; do echo 'Waiting for load_and_modify to complete...'; sleep 5; done && python reconciliation.py"]

  extension:
    build: ./extension
    depends_on:
      - reconciliation
    volumes:
      - ${LOCAL_SHARED_DATA_PATH}:/app/shared
      - ${LOCAL_COMPLETION_DATA_PATH}:/app/completion
      - ${LOCAL_CSV_OUTPUT_DIR_PATH}:/app/csv_output_dir
    environment:
      - API_URL=${API_URL}
      - USERNAME=${USERNAME}
      - PASSWORD=${PASSWORD}
      - INPUT_PATH=${OUTPUT_PATH_SHARED}
      - OUTPUT_PATH=${OUTPUT_PATH_CSV}
    entrypoint: ["sh", "-c", "while [ ! -f /app/completion/reconciliation_done ]; do echo 'Waiting for reconciliation to complete...'; sleep 5; done && python extension.py"]

volumes:
  shared_data:
  completion_data:
```

## Running the Pipeline

1. **Clone the Repository**

   Clone this repository to your local machine.

   ```sh
   git clone https://github.com/your-repository/semtui_pipeline.git
   cd semtui_pipeline
   ```

2. **Create Required Directories**

   Ensure the directories specified in the `.env` file are created on your local machine:

   ```sh
   mkdir -p /path/to/your/project/pipeline_results/shared_data
   mkdir -p /path/to/your/project/pipeline_results/csv_output_dir
   mkdir -p /path/to/your/project/pipeline_results/completion_data
   ```

3. **Build and Run the Docker Containers**

   Use Docker Compose to build and run the containers:

   ```sh
   docker-compose up --build
   ```

4. **Check Output**

   After the pipeline completes, the extended CSV file will be available in the specified output directory:

   ```sh
   /path/to/your/project/pipeline_results/csv_output_dir/extended_data.csv
   ```

## Troubleshooting

- If the pipeline fails at any step, check the logs of the respective container for error messages:
  
  ```sh
  docker logs <container_name>
  ```

- Ensure that the API URL and credentials are correct in the `.env` file.
- Verify that all necessary directories exist and are correctly mapped in the Docker Compose file.

## Conclusion

This setup ensures a streamlined and automated workflow for data processing, reconciliation, and extension using the SEMTUI framework. By following the steps outlined in this guide, you can efficiently manage and execute the data pipeline.