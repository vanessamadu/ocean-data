import numpy as np
import xarray as xr

def cyclostrophic_correction(u, v, ug, vg, f_lookup):

    du_dx = np.gradient(u, 0.125,axis=-1)
    du_dy = np.gradient(u, 0.125,axis=-2)
    dv_dx = np.gradient(v, 0.125,axis=-1)
    dv_dy = np.gradient(v, 0.125,axis=-2)
    print('gradients computed successfully')
    
    u_dot_grad_u_x = u * dv_dx + v * dv_dy
    u_dot_grad_u_y = u * du_dx + v * du_dy

    for ii in range(len(ug.coords['latitude'].values)):

        lat = ug.coords['latitude'].values[ii]
        f = f_lookup[lat]
        if np.abs(lat) < 15:
            # cyclostrophic corrections are only made from latitudes greater than 15 degrees north
            u_dot_grad_u_x[:,ii,:] = 0
            u_dot_grad_u_y[:,ii,:] = 0
        else:
            u_dot_grad_u_x[:,ii,:]/=f
            u_dot_grad_u_y[:,ii,:]/=f

    corrected_u = ug - u_dot_grad_u_x
    corrected_v = vg + u_dot_grad_u_y
    
    return corrected_u, corrected_v

def iterate_until_convergence(u, v, ug, vg, f_lookup, tolerance=0.01, max_iterations=100):
    for iteration in range(max_iterations):
        print(f"iteration: {iteration}")
        u_new, v_new = cyclostrophic_correction(u, v, ug, vg, f_lookup)
        diff_u = np.nanmax(np.abs(u_new - u))
        diff_v = np.nanmax(np.abs(v_new - v))
        
        if diff_u < tolerance and diff_v < tolerance:
            print(f"Converged after {iteration} iterations")
            break
        print(f"iteration did not converge: diff_u = {diff_u}, diff_v = {diff_v}")
        u, v = u_new, v_new
    
    return u, v

def sst_gradient(sst,output_directory):

    sst_gradient_x = np.gradient(data_array,axis=-1)
    sst_gradient_y = np.gradient(data_array,axis=-2)

    # create data arrays
    sst_gradient_x_da = xr.DataArray(sst_gradient_x,coords=data_array.coords,dims=data_array.dims,name='sst_gradient_x')
    sst_gradient_y_da = xr.DataArray(sst_gradient_y,coords=data_array.coords,dims=data_array.dims,name= 'sst_gradient_y')

    # create dataset
    data_array = xr.Dataset(
        {
            'sst_gradient_x':sst_gradient_x_da,
            'sst_gradient_y':sst_gradient_y_da
        }
    )

    # set attributes for the gradient variables
    data_array['sst_gradient_x'].attrs = {
        'units': 'K/m',
        'long_name': 'SST Gradient in X direction'
    }
    data_array['sst_gradient_y'].attrs = {
        'units': 'K/m',
        'long_name': 'SST Gradient in Y direction'
    }

    # Set global attributes
    data_array.attrs = {
        'title': 'Sea Surface Temperature Gradients',
        'institution': 'Imperial College London',
        'source': 'Derived from SST data',
        'history': 'Created on ' + str(np.datetime64('today')),
        'references': '[ADD REFERENCES]'
    }
    
    sst_gradient_ds.to_netcdf(f'{output_directory}/derived_sst_gradients.nc')
