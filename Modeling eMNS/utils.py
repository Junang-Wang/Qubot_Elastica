import numpy as np
def curl(A_field):
    '''
    A_field: (Dimensions, grid_x, grid_y, grid_z)
    '''
    B_field = np.gradient(A_field,1)