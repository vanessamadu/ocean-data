from astropy.convolution import convolve
import numpy as np
import xarray as xr
from scipy.ndimage import convolve1d

def stencil_mask(row,kernel_len):
    nans = np.isnan(row)
    mask = np.nan*np.ones(len(row))
    num_neighbours = int(np.floor(kernel_len/2))
    for ii in range(num_neighbours,len(nans)-num_neighbours):
        indices = [val for val in range(ii-num_neighbours,ii+num_neighbours+1)]
        indices.pop(num_neighbours)
        stencil_is_valid = np.array(not nans[indices].any())
        if stencil_is_valid:
            mask[ii] = stencil_is_valid
    return mask

def diff1d(row,h):
    ''' 
    len(row) >= 5
    '''
    # define kernels
    kernel_stencil = np.array([1/(12*h),-8/(12*h),0, 8/(12*h),-1/(12*h)])[::-1]
    kernel_central = np.array([-1/(2*h),0,1/(2*h)])[::-1]
    kernel_onesided = np.array([-1/h,1/h])[::-1]
    # evaluate derivatives
    dx_stencil = stencil_mask(row,len(kernel_stencil))*convolve(row,kernel_stencil,normalize_kernel=False,nan_treatment='fill',boundary=None,
                        mask=np.isnan(row))
    dx_central = stencil_mask(row,len(kernel_central))*convolve(row,kernel_central,normalize_kernel=False,nan_treatment='fill',boundary=None,
                        mask=np.isnan(row))
    dx_right = convolve1d(row,kernel_onesided,mode="constant",cval=np.nan)
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

def sst_gradient(SST_array):
    
    # metadata
    h = 0.05
    lat,lon = SST_array.indexes.values()

    # initialisation
    SST_grad_array_x = np.zeros(SST_array.shape)
    SST_grad_array_y = np.zeros(SST_array.shape)

    for ii in range(len(lat)):
        sst_at_lat = SST_array.isel(latitude = ii)
        SST_grad_array_x[ii,:] = diff1d(sst_at_lat,h)
        print(f"lat:{lat[ii]} complete")
    
    for jj in range(len(lon)):
        sst_at_lon = SST_array.isel(longitude = jj)
        SST_grad_array_y[:,jj] = diff1d(sst_at_lon,h)*-1
        print(f"lon:{lon[jj]} complete")
    return SST_grad_array_x,SST_grad_array_y


def sst_gradient_to_da(sst,output_directory,output_filename):

    sst_gradient_x, sst_gradient_y = sst_gradient(sst)

    # create data arrays
    sst_gradient_x_da = xr.DataArray(sst_gradient_x,coords=sst.coords,dims=sst.dims,name='sst_gradient_x')
    sst_gradient_y_da = xr.DataArray(sst_gradient_y,coords=sst.coords,dims=sst.dims,name= 'sst_gradient_y')

    # create dataset
    sst_gradient_ds = xr.Dataset(
        {
            'sst_gradient_x':sst_gradient_x_da,
            'sst_gradient_y':sst_gradient_y_da
        }
    )

    # set attributes for the gradient variables
    sst_gradient_ds['sst_gradient_x'].attrs = {
        'units': 'K/m',
        'long_name': 'SST Gradient in X direction'
    }
    sst_gradient_ds['sst_gradient_y'].attrs = {
        'units': 'K/m',
        'long_name': 'SST Gradient in Y direction'
    }

    # Set global attributes
    sst_gradient_ds.attrs = {
        'title': 'Sea Surface Temperature Gradients',
        'institution': 'Imperial College London',
        'source': 'Derived from SST data',
        'history': 'Created on ' + str(np.datetime64('today')),
        'references': '[ADD REFERENCES]'
    }
    
    sst_gradient_ds.to_netcdf(f'{output_directory}/{output_filename}')
