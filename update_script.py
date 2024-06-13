from json_functions import read_json_to_dataframe, update_json_file
import os

def load_metadata(filename):
    root_path = os.path.dirname(__file__)
    file_path = os.path.join(root_path, 'metadata\\%s'%filename)

    with open(file_path, 'r') as file:
        return(file.read()) 

print(load_metadata("data.py"))