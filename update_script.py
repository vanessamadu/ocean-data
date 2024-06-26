from json_functions import update_json_file
from data_module_list import *
import json

# script to update the ocean data reference guide json file

filename = "ocean_data.json"
with open(filename, "w") as file:
        json.dump([], file,indent=4)
for dataname in data_names:
    data = dataname.dataset
    update_json_file(filename,data)
