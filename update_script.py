from json_functions import read_json_to_dataframe, update_json_file
from data_module_list import *

data = metadata.data1.dataset
filename = "ocean_data.json"
update_json_file(filename,data)
