import json
import os
import pandas as pd

def update_json_file(filename:str, new_data:list):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    # Append the new data to the existing data
    existing_data.extend(new_data)

    # Write the updated data back to the JSON file
    with open(filename, "w") as file:
        json.dump(existing_data, file,indent=4)

def read_json_to_dataframe(filename:str):
    with open(filename, "r") as file:
        data = json.load(file)
    
    # Convert the JSON data to a DataFrame
    df = pd.DataFrame(data)
    return df