from json_functions import read_json_to_dataframe, update_json_file
from data_module_list import *

filename = "ocean_data.json"
for dataname in data_names:
    data = dataname.dataset
    update_json_file(filename,data)
