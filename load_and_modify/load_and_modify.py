import os
import pandas as pd
from semtui_refactored.data_modifier import DataModifier
from semtui_refactored.token_manager import TokenManager
from semtui_refactored.dataset_manager import DatasetManager

# Load environment variables
API_URL = os.getenv('API_URL', 'http://192.168.99.175:3003/api/')
USERNAME = os.getenv('USERNAME', 'test')
PASSWORD = os.getenv('PASSWORD', 'test')
CSV_FILE_PATH = os.getenv('CSV_FILE_PATH', '/app/csv_dir/JOT sample original.csv')
OUTPUT_PATH = os.getenv('OUTPUT_PATH', '/app/shared/processed_data.json')
DATASET_ID = os.getenv('DATASET_ID', '30')
TABLE_NAME = os.getenv('TABLE_NAME', 'New_Table3')
COMPLETION_FILE = '/app/completion/load_and_modify_done'

def initialize_managers(api_url, username, password):
    signin_data = {"username": username, "password": password}
    signin_headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    token_manager = TokenManager(api_url, signin_data, signin_headers)
    token = token_manager.get_token()
    
    dataset_manager = DatasetManager(api_url, token_manager)
    
    return dataset_manager

def read_and_process_csv(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
        print("CSV file imported successfully!")
        df = DataModifier.iso_date(df, date_col='Fecha_id')
        print("Data processed successfully!")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error reading or processing CSV file: {e}")
        return None

def main():
    dataset_manager = initialize_managers(API_URL, USERNAME, PASSWORD)
    df = read_and_process_csv(CSV_FILE_PATH)
    
    if df is not None:
        try:
            dataset_manager.add_table_to_dataset(DATASET_ID, df, TABLE_NAME)
            print(f"Table '{TABLE_NAME}' added to dataset ID {DATASET_ID} successfully.")
            df.to_json(OUTPUT_PATH, orient='records')
            # Create completion file
            with open(COMPLETION_FILE, 'w') as f:
                f.write('done')
        except Exception as e:
            print(f"Error adding table to dataset: {e}")

if __name__ == "__main__":
    main()
