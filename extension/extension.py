import os
import json
from semtui_refactored.token_manager import TokenManager
from semtui_refactored.extension_manager import ExtensionManager
from semtui_refactored.utils import Utility

# Load environment variables
API_URL = os.getenv('API_URL', 'http://192.168.99.175:3003/api/')
USERNAME = os.getenv('USERNAME', 'test')
PASSWORD = os.getenv('PASSWORD', 'test')
RECONCILIATED_COLUMN_NAME = os.getenv('RECONCILIATED_COLUMN_NAME', 'City')
PROPERTIES = os.getenv('PROPERTIES', 'apparent_temperature_max,apparent_temperature_min,precipitation_sum').split(',')
NEW_COLUMNS_NAME = os.getenv('NEW_COLUMNS_NAME', 'Apparent_Max_Temperature,Apparent_Min_Temperature,Total_Precipitation').split(',')
DATE_COLUMN_NAME = os.getenv('DATE_COLUMN_NAME', 'Fecha_id')
ID_EXTENDER = os.getenv('ID_EXTENDER', 'meteoPropertiesOpenMeteo')
WEATHER_PARAMS = os.getenv('WEATHER_PARAMS', 'apparent_temperature_max,apparent_temperature_min,precipitation_sum').split(',')
INPUT_PATH = os.getenv('INPUT_PATH', '/app/shared/reconciled_data.json')
OUTPUT_PATH = os.getenv('OUTPUT_PATH', '/app/csv_output_dir/extended_data.csv')
COMPLETION_FILE = '/app/completion/extension_done'

def initialize_managers(api_url, username, password):
    signin_data = {"username": username, "password": password}
    signin_headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    token_manager = TokenManager(api_url, signin_data, signin_headers)
    token = token_manager.get_token()
    
    extension_manager = ExtensionManager(api_url, token)
    
    return extension_manager

def extend_column_and_save_to_csv(extension_manager, reconciled_data, reconciliated_column_name, id_extender, properties, new_columns_name, date_column_name, weather_params, output_path):
    try:
        # Ensure that reconciled_data is in the expected format
        if 'raw' in reconciled_data and isinstance(reconciled_data['raw'], list):
            extended_table = extension_manager.extend_column(
                reconciled_data['raw'], 
                reconciliated_column_name, 
                id_extender, 
                properties, 
                new_columns_name, 
                date_column_name, 
                weather_params
            )
            if extended_table:
                print("Column extended successfully!")
                extended_df = Utility.load_json_to_dataframe(extended_table, georeference_data=True)
                print("Extended data loaded into DataFrame successfully!")
                extended_df.to_csv(output_path, index=False)
                print(f"Extended data saved to {output_path} successfully!")
                # Create completion file
                with open(COMPLETION_FILE, 'w') as f:
                    f.write('done')
                return extended_df
            else:
                print("Failed to extend column.")
                return None
        else:
            print("Unexpected data structure:", json.dumps(reconciled_data, indent=4))
            return None
    except Exception as e:
        print(f"Error extending column: {e}")
        return None

def main():
    extension_manager = initialize_managers(API_URL, USERNAME, PASSWORD)
    
    if not os.path.exists(INPUT_PATH):
        print(f"Input file {INPUT_PATH} does not exist.")
        return
    
    try:
        with open(INPUT_PATH, 'r') as json_file:
            reconciled_data = json.load(json_file)
        extend_column_and_save_to_csv(
            extension_manager, 
            reconciled_data, 
            RECONCILIATED_COLUMN_NAME, 
            ID_EXTENDER, 
            PROPERTIES, 
            NEW_COLUMNS_NAME, 
            DATE_COLUMN_NAME, 
            WEATHER_PARAMS, 
            OUTPUT_PATH
        )
    except Exception as e:
        print(f"Error reading input data: {e}")

if __name__ == "__main__":
    main()
