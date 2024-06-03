import os
import json
import requests
from semtui_refactored.token_manager import TokenManager
from semtui_refactored.dataset_manager import DatasetManager
from semtui_refactored.reconciliation_manager import ReconciliationManager

# Load environment variables
API_URL = os.getenv('API_URL', 'http://192.168.99.175:3003/api/')
USERNAME = os.getenv('USERNAME', 'test')
PASSWORD = os.getenv('PASSWORD', 'test')
DATASET_ID = os.getenv('DATASET_ID', '30')
TABLE_NAME = os.getenv('TABLE_NAME', 'New_Table3')
COLUMN_NAME = os.getenv('COLUMN_NAME', 'City')
ID_RECONCILIATOR = os.getenv('ID_RECONCILIATOR', 'geocodingHere')
OUTPUT_PATH = os.getenv('OUTPUT_PATH', '/app/shared/reconciled_data.json')
COMPLETION_FILE = '/app/completion/reconciliation_done'

def initialize_managers(api_url, username, password):
    signin_data = {"username": username, "password": password}
    signin_headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    token_manager = TokenManager(api_url, signin_data, signin_headers)
    token = token_manager.get_token()
    
    dataset_manager = DatasetManager(api_url, token_manager)
    reconciliation_manager = ReconciliationManager(api_url, token_manager)
    
    return dataset_manager, reconciliation_manager

def reconcile_and_save(reconciliation_manager, table_data, column_name, id_reconciliator, output_path):
    try:
        print(f"Sending reconciliation request to API for column '{column_name}' with data: {json.dumps(table_data, indent=4)}")
        reconciled_table = reconciliation_manager.reconcile(table_data, column_name, id_reconciliator)
        if reconciled_table is not None:
            print("Column reconciled successfully!")
            with open(output_path, 'w') as json_file:
                json.dump(reconciled_table, json_file, indent=4)
            print(f"Reconciled data saved to {output_path}")
            # Create completion file
            with open(COMPLETION_FILE, 'w') as f:
                f.write('done')
        else:
            print("Failed to reconcile column.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending reconciliation request: {e.response.text}")
    except Exception as e:
        print(f"Error reconciling column: {e}")

def main():
    dataset_manager, reconciliation_manager = initialize_managers(API_URL, USERNAME, PASSWORD)
    
    try:
        table_data = dataset_manager.get_table_by_name(DATASET_ID, TABLE_NAME)
        if table_data:
            print(f"Table '{TABLE_NAME}' retrieved successfully!")
            reconcile_and_save(reconciliation_manager, table_data, COLUMN_NAME, ID_RECONCILIATOR, OUTPUT_PATH)
        else:
            print(f"Table '{TABLE_NAME}' not found in the dataset.")
    except Exception as e:
        print(f"Error retrieving table '{TABLE_NAME}': {e}")

if __name__ == "__main__":
    main()
