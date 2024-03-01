import torch
def discrete_curl(A_field):
    '''
    A_field: (batch, Dimensions, grid_x, grid_y, grid_z)
    '''
    B_field = torch.gradient(A_field,spacing=1.0)