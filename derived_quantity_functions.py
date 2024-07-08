import numpy as np
import xarray as xr

def cyclostrophic_correction(u, v, ug, vg, f_lookup,flags):

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

    corrected_u = np.where(flags,ug - u_dot_grad_u_x,u)
    corrected_v = np.where(flags,vg + u_dot_grad_u_y,v)
    print("corrections computed successfully")
    return corrected_u, corrected_v

def iterate_until_convergence(u, v, ug, vg, f_lookup, tolerance=0.1, max_iterations=100):
    # initialise
    flags = np.ones(u.shape)
    u_old = u
    v_old = v
    norm_diff_old = np.sqrt(np.square(u_old) + np.square(v_old))
    print(norm_diff_old)
    ii = 0
    for iteration in range(max_iterations):
        print(f"iteration: {iteration}")

        # new iterates
        u_new, v_new = cyclostrophic_correction(u_old,v_old,ug,vg,f_lookup,flags)
        diff_u = u_new - u_old
        diff_v = v_new - v_old
        norm_diff_new = np.sqrt(np.square(diff_u)+np.square(diff_v))
        print(norm_diff_old-norm_diff_new)
        if ii >0:
            flags = np.logical_and(norm_diff_new > tolerance,norm_diff_old>norm_diff_new)
        print(f"number of terms that have not converged:{int(np.sum(flags))}")

        if (np.ones(flags.shape)-flags).all():
            print(f"Converged after {iteration} iterations")
            break
        #print(f"iteration did not converge: diff_u = {diff_u}, diff_v = {diff_v}")
        u_old, v_old = u_new, v_new
        norm_diff_old = norm_diff_new
        ii+=1
    
    return u, v

#-------------------- SST GRADIENT HELPER FUNCTIONS -----------------------#

def forward_difference(next,now,h):
    '''
    next:   SST at the next grid point
    now:    SST at the current grid point
    h:      grid space
    '''
    return (next-now)/h

def backward_difference(now,prev,h):
    '''
    now:    SST at the current grid point
    prev:   SST at the previous grid point
    h:      grid space
    '''
    return (now-prev)/h

def central_difference(next,prev,h):
    '''
    next:   SST at the next grid point
    prev:   SST at the previous grid point
    h:      grid space
    '''
    return (next-prev)/(2*h)

def five_point_stencil(next,next_next,prev,prev_prev,h):
    '''
    next:       SST at the next grid point
    next_next:  SST at the next grid point after `next`
    prev:       SST at the previous grid point
    prev:       SST at the previous grid point before `prev`
    h:          grid space
    '''
    return (prev_prev-next_next+ 8*next - 8*prev)/(12*h)


def sst_gradient(sst,output_directory,output_filename):

    sst_gradient_x = np.gradient(sst,axis=-1)
    sst_gradient_y = np.gradient(sst,axis=-2)

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
