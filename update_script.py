from json_functions import read_json_to_dataframe, update_json_file
from data_module_list import *
import json

filename = "ocean_data.json"
with open(filename, "w") as file:
        json.dump([], file,indent=4)
for dataname in data_names:
    data = dataname.dataset
    update_json_file(filename,data)
