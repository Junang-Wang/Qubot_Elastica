import torch
import matplotlib.pyplot as plt
def compute_discrete_curl(A_field, device):
    '''
    A_field: (batch, Dimensions, grid_x, grid_y, grid_z)
    '''
    batch, dimensions, grid_x, grid_y, grid_z = A_field.shape
    discrete_curl = torch.zeros(batch, dimensions, grid_x, grid_y, grid_z, device=device)

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

def gridData_reshape(data):
    '''
    reshape data shape from ( dimension, grid_x, grid_y, grid_z) to (-1,dimension)
    '''
    return torch.flatten(data.permute(1,2,3,0), start_dim=0, end_dim=-2) #(-1, dimension)


def plot_3D_vector_field(position, vectorField, figsize=(5,5), length=1):
    '''
    Plot 3D vector field
    -----------input----------
    position: position of grids shape: (1,dimensions,grid_x,grid_y,grid_z)
    vectorField: shape (1,dimensions,grid_x,grid_y,grid_z)
    '''
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111,projection='3d') 
    p = gridData_reshape(position) #(-1, dimension)
    vector = gridData_reshape(vectorField) #(-1, dimension)

    ax.quiver(p[:,0], p[:,1], p[:,2], vector[:,0], vector[:,1], vector[:,2], length=length)
    plt.show()

def denorm(x, Bmax, Bmin):
    '''
    This function de-normalize the max-min normalization
    x = 0.5*(x_norm+1)*(Bmax-Bmin) - Bmin
    '''
    x_norm = 0.5*(x+1)*(Bmax.expand_as(x_norm)-Bmin.expand_as(x_norm)) - Bmin.expand_as(x_norm)
    return x_norm


