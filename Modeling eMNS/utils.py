import torch
def compute_discrete_curl(A_field):
    '''
    A_field: (batch, Dimensions, grid_x, grid_y, grid_z)
    '''
    batch, dimensions, grid_x, grid_y, grid_z = A_field.shape
    discrete_curl = torch.zeros(batch, dimensions, grid_x, grid_y, grid_z)

    # grad_x_A: dA/dx, grad_y_A: dA/dy, grad_z_A: dA/dz
    _,_, grad_x_A, grad_y_A, grad_z_A = torch.gradient(A_field,spacing=1.0)

    # curl A = (dA_z/dy - dA_y/dz) i + (dA_x/dz - dA_z/dx) j + (dA_y/dx - dA_x/dy) z
    discrete_curl[:,0] = grad_y_A[:,2] - grad_z_A[:,1]
    discrete_curl[:,1] = grad_z_A[:,0] - grad_x_A[:,2]
    discrete_curl[:,2] = grad_x_A[:,1] - grad_y_A[:,0]

    return discrete_curl

def compute_discrete_divergence(A_field):
    '''
    A_field: (batch, dimensions, grid_x, grid_y, grid_z)
    '''
    batch, dimensions, grid_x, grid_y, grid_z = A_field.shape
    discrete_div = torch.zeros(batch, 1, grid_x, grid_y, grid_z)
    
    # grad_x_A: dA/dx, grad_y_A: dA/dy, grad_z_A: dA/dz
    _,_, grad_x_A, grad_y_A, grad_z_A = torch.gradient(A_field,spacing=1.0)
    
    # div A = dA_x/dx  + dA_y/dy  + dA_z/dz 
    discrete_div[:,0] = grad_x_A[:,0] + grad_y_A[:,1] + grad_z_A[:,2]
    return discrete_div
