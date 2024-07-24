from astropy.convolution import convolve
import numpy as np
from scipy.ndimage import convolve1d

def stencil_mask(x,kernel_len):
    nans = np.isnan(x)
    mask = np.nan*np.ones(len(x))
    num_neighbours = int(np.floor(kernel_len/2))
    for ii in range(num_neighbours,len(nans)-num_neighbours):
        indices = [val for val in range(ii-num_neighbours,ii+num_neighbours+1)]
        indices.pop(num_neighbours)
        stencil_is_valid = np.array(not nans[indices].any())
        if stencil_is_valid:
            mask[ii] = stencil_is_valid
    return mask

x = np.array([1.0,2.0,4.0,5.0,7.0,np.nan,3.0,6.0])

def diff1d(row):
    ''' 
    len(row) >= 5
    '''
    # define kernels
    kernel_stencil = np.array([1/12,-8/12,0, 8/12,-1/12])[::-1]
    kernel_central = np.array([-0.5,0,0.5])[::-1]
    kernel_onesided = np.array([-1.0,1.0])[::-1]
    # evaluate derivatives
    dx_stencil = stencil_mask(x,len(kernel_stencil))*convolve(x,kernel_stencil,normalize_kernel=False,nan_treatment='fill',boundary=None,
                        mask=np.isnan(x))
    dx_central = stencil_mask(x,len(kernel_central))*convolve(x,kernel_central,normalize_kernel=False,nan_treatment='fill',boundary=None,
                        mask=np.isnan(x))
    dx_right = convolve1d(x,kernel_onesided,mode="constant",cval=np.nan)
    dx_left = np.roll(dx_right,shift=1,axis=0)

    # print(f"x: {x}")
    # print(f"dx_stencil: {dx_stencil}")
    # print(f"dx_central: {dx_central}")
    # print(f"dx_left: {dx_left}")
    # print(f"dx_right: {dx_right}")

    dx = np.where(np.isnan(dx_stencil),dx_central,dx_stencil)
    dx = np.where(np.isnan(dx),dx_left,dx)
    dx = np.where(np.isnan(dx),dx_right,dx)

    return(dx)

