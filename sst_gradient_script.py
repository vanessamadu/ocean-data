import time
from derived_quantity_functions import *

start = time.time()

filename="CMEMS_West_NA_sst_2012_2022.nc"
file_directory = "D:\PhD\ocean-datasets\copernicus-data"
# Load the NetCDF file
data_path = f"{file_directory}/{filename}"
dataset = xr.open_dataset(data_path)

sst = dataset['analysed_sst'].isel(time=0)
sst_gradient(sst,'./','sst_x_gradients_with_boundaries.nc')
end = time.time()
print(end-start)