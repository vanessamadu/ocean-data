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

