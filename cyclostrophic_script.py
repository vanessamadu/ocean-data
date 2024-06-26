from derived_quantity_functions import *
import xarray as xr

output_directory = "D:\PhD\ocean-datasets\copernicus-data"
velocities_filename="CMEMS_West_NA_currents_2012_2023"

# load the NetCDF file
data_path = f"{output_directory}/{velocities_filename}"
dataset = xr.open_dataset(data_path)

# extract data
ugosa = dataset["ugosa"]
vgosa = dataset["vgosa"]
omega = 7.3e-5 
''' Citation: George R. Sell,
Chapter 6 - The Foundations of Oceanic Dynamics and Climate Modeling,
Editor(s): S. Friedlander, D. Serre,
Handbook of Mathematical Fluid Dynamics,
North-Holland,
Volume 4,
2007,
Pages 331-405,
ISSN 1874-5792,
ISBN 9780444528346,
https://doi.org/10.1016/S1874-5792(07)80010-3.
(https://www.sciencedirect.com/science/article/pii/S1874579207800103)
Keywords: planetary motion; quasi periodic forcing; skew product dynamics; thin domain dynamics
'''
f = [2*omega*np.sin(theta) for theta in ugosa.coords['latitude'].values]

# initialise
u = ugosa.copy()
v = vgosa.copy()