import copernicusmarine
import pandas as pd
import glob
import xarray as xr
import os


# scripts for accessing the Copernicus Python API to download data subsets
def generate_daily_timestamps(start_date, end_date):
    return pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y-%m-%d 00:00:00').tolist()

# subset request parameters
options = ['short_geostrophic_velocities','short_wind','long_geostrophic_velocities','long_wind','long_sst','short_sst']
toggle = options[3]
output_directory = "D:\PhD\ocean-datasets\copernicus-data"

if toggle == 'short_geostrophic_velocities':
    # SHORT TIME FRAME: 11/03/2022 - 22/06/2024
    dataset_id = "cmems_obs-sl_glo_phy-ssh_nrt_allsat-l4-duacs-0.25deg_P1D"
    variables = ["ugos","vgos","ugosa", "vgosa","err_ugosa","err_vgosa"]
    # West NA
    min_lon, max_lon = -83, -40 
    min_lat, max_lat = 0, 60
    start_date, end_date = "2022-03-11 12:00:00", "2024-06-22 23:00:00"
    min_depth, max_depth = 0, 15
    output_filename = "CMEMS_West_NA_currents_2022_2024.nc"

    # Request subset
    # Read credentials from environment variables
    copernicusmarine.subset(
        dataset_id=dataset_id,
        variables=variables,
        minimum_longitude=min_lon,
        maximum_longitude=max_lon,
        minimum_latitude=min_lat,
        maximum_latitude=max_lat,
        start_datetime=start_date,
        end_datetime=end_date,
        minimum_depth=min_depth,
        maximum_depth=max_depth,
        output_filename=output_filename,
        output_directory=output_directory,
    )

elif toggle == 'short_wind':
    # SHORT TIME FRAME: 11/03/2022 - 22/06/2024
    dataset_id = "cmems_obs-wind_glo_phy_nrt_l4_0.125deg_PT1H"
    variables = ["eastward_wind", "northward_wind","eastward_stress","northward_stress", "wind_curl","wind_divergence"]
    # West NA
    min_lon, max_lon = -83, -40 
    min_lat, max_lat = 0, 60
    start_date, end_date = "2024-02-01 00:00:00", "2024-06-22 23:00:00"
    output_filename = "Full_CMEMS_West_NA_wind_2022_2024.nc"
    timestamps = generate_daily_timestamps(start_date, end_date)

    # Request subset for each timestamp
    for timestamp in timestamps:
        # Read credentials from environment variables
        copernicusmarine.subset(
            dataset_id=dataset_id,
            variables=variables,
            minimum_longitude=min_lon,
            maximum_longitude=max_lon,
            minimum_latitude=min_lat,
            maximum_latitude=max_lat,
            start_datetime=timestamp,
            end_datetime=timestamp,
            output_filename=f"CMEMS_West_NA_wind_{timestamp.replace(':', '').replace('-', '')}.nc",
            output_directory=output_directory,
        )
    # List of all downloaded filesy
    file_paths = sorted(glob.glob(f"{output_directory}/CMEMS_West_NA_wind_*.nc"))

    # Open multiple files as a single dataset
    datasets = [xr.open_dataset(file) for file in file_paths]
    combined_dataset = xr.concat(datasets, dim='time')

    # Save the combined dataset to a new NetCDF file
    combined_dataset.to_netcdf(f"{output_filename}")
    for file_path in file_paths:
        os.remove(file_path)

elif toggle == "long_geostrophic_velocities":
    # LONGER TIME FRAME 01/01/2012 - 08/09/2023
    dataset_id = "cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.25deg_P1D"
    variables = ["ugos","vgos","ugosa", "vgosa","err_ugosa","err_vgosa"]
    # West NA
    min_lon, max_lon = -83, -40 
    min_lat, max_lat = 0, 60
    start_date, end_date = "2012-01-01 00:00:00", "2023-09-08 23:00:00"
    min_depth, max_depth = 0, 15
    output_filename = "CMEMS_West_NA_currents_2012_2023.nc"

    # Request subset
    copernicusmarine.subset(
        dataset_id=dataset_id,
        variables=variables,
        minimum_longitude=min_lon,
        maximum_longitude=max_lon,
        minimum_latitude=min_lat,
        maximum_latitude=max_lat,
        start_datetime=start_date,
        end_datetime=end_date,
        minimum_depth=min_depth,
        maximum_depth=max_depth,
        output_filename=output_filename,
        output_directory=output_directory,
    )

elif toggle == 'long_wind':
# LONGER TIME FRAME 01/01/2012 - 08/09/2023
    dataset_id = "cmems_obs-wind_glo_phy_my_l4_0.125deg_PT1H"
    variables = ["eastward_wind", "northward_wind","eastward_stress","northward_stress", "wind_curl","wind_divergence"]
    # West NA
    min_lon, max_lon = -83, -40 
    min_lat, max_lat = 0, 60
    start_date, end_date = "2020-04-25 00:00:00", "2023-09-08 23:00:00"
    output_filename = "Full_CMEMS_West_NA_wind_2012_2023.nc"
    timestamps = generate_daily_timestamps(start_date, end_date)


    # Request subset for each timestamp
    for timestamp in timestamps:
        # Read credentials from environment variables
        copernicusmarine.subset(
            dataset_id=dataset_id,
            variables=variables,
            minimum_longitude=min_lon,
            maximum_longitude=max_lon,
            minimum_latitude=min_lat,
            maximum_latitude=max_lat,
            start_datetime=timestamp,
            end_datetime=timestamp,
            output_filename=f"CMEMS_West_NA_wind_{timestamp.replace(':', '').replace('-', '')}.nc",
            output_directory=output_directory,
            force_download= True,
            dataset_version="202211",
            dataset_part="default",
            service= "arco-geo-series"
        )
    # List of all downloaded filesy
    file_paths = sorted(glob.glob(f"{output_directory}/CMEMS_West_NA_wind_*.nc"))

    # Open multiple files as a single dataset
    datasets = [xr.open_dataset(file) for file in file_paths]
    combined_dataset = xr.concat(datasets, dim='time')

    # Save the combined dataset to a new NetCDF file
    combined_dataset.to_netcdf(f"{output_filename}")
    for file_path in file_paths:
        os.remove(file_path)
    
elif toggle == 'long_sst':
    # LONGER TIME FRAME 01/01/2012 - 08/09/2023
    dataset_id = "METOFFICE-GLO-SST-L4-REP-OBS-SST"
    variables = ["analysed_sst","analysis_error"]
    # West NA
    min_lon, max_lon = -83, -40 
    min_lat, max_lat = 0, 60
    start_date, end_date = "2012-01-01 00:00:00", "2022-05-31 23:00:00"
    output_filename = "CMEMS_West_NA_sst_2012_2022.nc"

    # Request subset
    copernicusmarine.subset(
        dataset_id=dataset_id,
        variables=variables,
        minimum_longitude=min_lon,
        maximum_longitude=max_lon,
        minimum_latitude=min_lat,
        maximum_latitude=max_lat,
        start_datetime=start_date,
        end_datetime=end_date,
        output_filename=output_filename,
        output_directory=output_directory,
    )

elif toggle == 'short_sst':
     # SHORT TIME FRAME: 11/03/2022 - 18/06/2024
    dataset_id = "METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2"
    variables = ["analysed_sst","analysis_error"]
    # West NA
    min_lon, max_lon = -83, -40 
    min_lat, max_lat = 0, 60
    start_date, end_date = "2022-03-11 00:00:00", "2024-06-18 23:00:00"
    output_filename = "CMEMS_West_NA_sst_2022_2024.nc"

    # Request subset
    copernicusmarine.subset(
        dataset_id=dataset_id,
        variables=variables,
        minimum_longitude=min_lon,
        maximum_longitude=max_lon,
        minimum_latitude=min_lat,
        maximum_latitude=max_lat,
        start_datetime=start_date,
        end_datetime=end_date,
        output_filename=output_filename,
        output_directory=output_directory,
    )