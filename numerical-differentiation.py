import numpy as np
import xarray as xr

# ======== Differencing Functions ======== #
def one_sided_difference(first,second,h):
    '''
    first:     SST at the first grid point
    second:    SST at the second grid point
    h:         grid space
    '''
    return (second-first)/h

def central_difference(next,prev,h):
    '''
    next:   SST at the next grid point
    prev:   SST at the previous grid point
    h:      grid spacing
    '''
    return (next-prev)/(2*h)

def five_point_stencil(next,next_next,prev,prev_prev,h):
    '''
    next:       SST at the next grid point
    next_next:  SST at the next grid point after `next`
    prev:       SST at the previous grid point
    prev:       SST at the previous grid point before `prev`
    h:          grid spacing
    '''
    return (prev_prev-next_next+ 8*next - 8*prev)/(12*h)

# ========== Boundary Differencing ========== #
def boundary_difference(boundary,h,SST_array,N,ii):
    if boundary == "W" or boundary == "S":
        index_array = [0,1]
        ii = 0
    elif boundary == "E" or boundary == "N":
        index_array = [N-2,N-1]
        ii = N-1
    # assigned values to points array:
    if boundary == "N" or boundary == "S":
        points_array = SST_array.isel(latitude = index_array,longitude = ii).values
    elif boundary == "E" or boundary == "W":
        points_array = SST_array.isel(latitude = ii,longitude = index_array).values
    # 
    nans = np.isnan(np.array(points_array))
    if np.sum(nans)==0:
        first,second = points_array[index_array]
    
    return one_sided_difference(first,second,h)
    
