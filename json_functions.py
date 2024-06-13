import json
import os

def update_json_file(filename, new_data):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append the new data to the existing data
    existing_data.extend(new_data)

    # Write the updated data back to the JSON file
    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)
