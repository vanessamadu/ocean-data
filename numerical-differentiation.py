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