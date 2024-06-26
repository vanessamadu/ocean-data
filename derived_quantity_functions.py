import numpy as np

def cyclostrophic_correction(u, v, ug, vg, f):

    du_dx = np.gradient(u, axis=-1)
    du_dy = np.gradient(u, axis=-2)
    dv_dx = np.gradient(v, axis=-1)
    dv_dy = np.gradient(v, axis=-2)
    
    u_dot_grad_u_x = u * dv_dx + v * dv_dy
    u_dot_grad_u_y = u * du_dx + v * du_dy
    
    corrected_u = ug - (1 / f) * u_dot_grad_u_x
    corrected_v = vg + (1 / f) * u_dot_grad_u_y
    
    return corrected_u, corrected_v

def iterate_until_convergence(u, v, ug, vg, f, tolerance=0.01, max_iterations=100):
    for iteration in range(max_iterations):
        u_new, v_new = cyclostrophic_correction(u, v, ug, vg, f)
        
        diff_u = np.max(np.abs(u_new - u))
        diff_v = np.max(np.abs(v_new - v))
        
        if diff_u < tolerance and diff_v < tolerance:
            print(f"Converged after {iteration} iterations")
            break
        
        u, v = u_new, v_new
    
    return u, v