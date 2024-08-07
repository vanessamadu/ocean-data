"""
Script Name: butterworth.py
Description: Applies a local Butterworth filter to drifter data based on drifter latitude

Acknowledgment:
This code is an iteration of the original code written by Dr Michael O'Malley to process data for the paper 
"Multivariate Probabilistic Regression with Natural Gradient Boosting". Special thanks to Michael O'Malley for 
providing the foundational code and methodologies that have been adapted in this script.

Author: Vanessa Madu
Date: 30/07/2024
Version: 1.0
"""

# dependent modules
import numpy as np
import pandas as pd
from scipy import signal
# for info
import time
def identify_time_series_segments(timevec:pd.Series,cut_off: int = 6) -> np.ndarray:
    """
    Segments a time series based on time gaps greater than the specified cutoff.

    Parameters:
    - timevec: A pandas Series of datetime values.
    - cut_off: An integer specifying the time gap cutoff in hours.

    Returns:
    - A numpy array with segment IDs for each time point in the input series.
    """
    times = timevec.values
    time_gaps = np.diff(timevec)
    mask = time_gaps > np.timedelta64(cut_off,'h') # identify where time gap is > than 'cut_off' hours
    mask = np.insert(mask,0,False)
    segments = np.cumsum(mask)
    return segments

def butterworth_filter(time_series: np.ndarray, latitude: np.ndarray, order: int=5) -> np.ndarray: 
    """
    Applies a 1D Butterworth filter to each column of the input time series data.

    Parameters:
    - ts: A 2D numpy array of shape (N, P) where N is the number of time points and P is the number of variables.
    - latitude: A 1D numpy array of latitude values corresponding to each time point.
    - order: An integer specifying the order of the Butterworth filter.

    Returns:
    - A 2D numpy array of the same shape as the input array, with filtered data.
    """
    time_series_len = time_series.shape[0]
    num_time_series = time_series.shape[1]
    dtype = time_series.dtype
    # initialise output with same shape and dtype as input
    out = np.zeros(time_series.shape,dtype=dtype) 
    # temporarily set missing values to zero
    nan_mask = np.isnan(time_series)
    # prevent changes to the time series outside of this function
    time_series = time_series.copy()
    time_series[nan_mask] = 0

    sample_freq = 1/(6*60*60) #Hz
    nyquist_freq = 0.5*sample_freq 

    if time_series_len < order * 6:
        out = out*np.nan # discard time series segment
    else:
        # perform daily filtering (moving BW filter over four six hourly observations)
        for ii in range(0,time_series_len,4):
            average_24_hour_lat = np.mean(latitude[ii:(ii+4)])
            # threshold frequency = minimum of intertial frequency/1.5 and once every five days
            earth_rotation_rate = 7.2921e-5
            inertial_freq = 2*earth_rotation_rate*np.sin(np.deg2rad(np.abs(average_24_hour_lat)))
            inertial_freq_hz = inertial_freq/(2*np.pi)
            five_day_freq_hz = 1 / (5 * 24 * 60 ** 2)
            threshold_freq = np.max([inertial_freq_hz/1.5, five_day_freq_hz]) 

            b,a = signal.butter(order,threshold_freq/nyquist_freq,btype='lowpass',analog=False)
            for jj in range(num_time_series):
                filtered_time_series = signal.filtfilt(b,a,time_series[:,jj])
                out[ii:(ii+4),jj] = filtered_time_series[ii:(ii+4)]
            out[nan_mask] = np.nan
    
    return out
            
def filter_covariates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the butterworth_filter function to each covariate column in the DataFrame.

    This function filters the 'u', 'v', 'Wx', 'Wy', 'Tx', and 'Ty' columns of the DataFrame,
    creating copies if they do not already exist, and replacing the filtered values back
    into the DataFrame.

    Parameters:
    - df: A pandas DataFrame containing the data to be filtered. The DataFrame must contain
          a 'lat' column and the columns specified in cols_to_filter.

    Returns:
    - A pandas DataFrame with the filtered data.
    """
    lat = df['lat'].values
    time_dependent_vars = ['u','v','Wx','Wy','Tx','Ty']

    # prevent changes to the data outside of this function
    for var in time_dependent_vars:
        if var + '_filtered' not in df.columns:
            df[var + '_filtered'] = df[var].copy()
    
    vars_to_filter = [var + '_filtered' for var in time_dependent_vars]
    time_series = df[vars_to_filter].values
    filtered_vars = butterworth_filter(time_series,lat)

    df[vars_to_filter] = filtered_vars
    return df

# ---------- FILTER SCRIPT ----------- #

def main():
    start_time = time.time()
    print('starting data processing')
    dataset = pd.read_hdf('drifter_full.h5')

    print('data loaded successfully')
    # convert from cm/s -> m/s and then divide by another 100 to correct the initial processing that
    # multiplied cm/s by 100 to get m/s...

    #using a small subset of the data for testing
    frac = 0.0005
    print(f'sampling {frac*100}% of the dataset')
    dataset = dataset.sample(frac=frac, random_state=42)
    print(f'new dataset shape: {dataset.shape}')
    dataset.loc[:, 'u']/=100**2
    dataset.loc[:, 'v']/=100**2

    # set extreme values to NaN
    for var in ['u','v','Tx','Ty','Wy','Wx']:
        extreme_val_mask = dataset[var] < -900
        dataset.loc[extreme_val_mask,var] = np.nan

    # discard observations with lat/lon variance estimate >= 0.5 degrees
    dataset = dataset.query('lon_var<0.5 and lat_var<0.5')
    # group the data for each drifter id into time series segments 
    dataset.loc[:,'segment_id'] = dataset.groupby('id').loc['time'].transform(identify_time_series_segments)
    filtered_dataset = dataset.groupby(['id', 'segment_id'], group_keys=False).apply(filter_covariates, include_groups=False)
    print('applied Butterworth filter to each segment')
    filtered_dataset.to_hdf(path_or_buf="filtered_data_test.h5", key="drifter", mode='w')
    print('saved filtered data')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Filtering {frac*100}% of the data took : {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main()