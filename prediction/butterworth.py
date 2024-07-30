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
import probdrift.oceanfns as ofn

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
    time_series_len = time_series.shape(0)
    num_time_series = time_series.shape(1)
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
            threshold_freq = ofn.get_cut_off(average_24_hour_lat)
            b,a = signal.butter(order,threshold_freq/nyquist_freq,btype='lowpass',analog=False)
            for jj in range(num_time_series):
                filtered_time_series = signal.filtfilt(b,a,time_series[:,jj])
                out[ii:(ii+4),jj] = filtered_time_series[ii:(ii+4),jj]
            out[nan_mask] = np.nan
    
    return out
            