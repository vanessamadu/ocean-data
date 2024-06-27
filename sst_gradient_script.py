from derived_quantity_functions import *

output_directory = "D:\PhD\ocean-datasets\copernicus-data"
filename_long = "CMEMS_West_NA_sst_2012_2022.nc"
filename_short = "CMEMS_West_NA_sst_2022_2024.nc"

output_filename_long = "derived_West_NA_sst_gradients_2012_2022.nc"
output_filename_short = "derived_West_NA_sst_gradients_2022_2024.nc"
# load the NetCDF file
data_path = f"{output_directory}/{filename_long}"
sst = xr.open_dataset(data_path)

sst_gradient(sst,output_directory,output_filename_short)
sst_gradient(sst,output_directory,output_filename_long)
