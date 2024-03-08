# Scalar Radial Basis Functions
import torch

def Gaussian(eps, x):
    return torch.exp(-eps*x**2)

def grad_Gaussian(eps,X):
    '''
    X = |x| * d|x|/d(x,y,z)
    '''
    return torch.exp(-2*eps*X)


def gridData_reshape(data):
    '''
    reshape data shape from ( dimension, grid_x, grid_y, grid_z) to (-1,dimension)
    '''
    return torch.flatten(data.permute(1,2,3,0), start_dim=0, end_dim=-2) #(-1, dimension)


def Euclidean_distance(samples_p, centers_p):
    '''
    centers_p: positions of radial kernel centers, shape: (1, dimension, grid_x, grid_y, grid_z)
    samples_p: positions of samples,               shape: (1, dimension, grid_x, grid_y, grid_z)
    Euclidean distance \sum_{i=dimensions}(\sqrt(r_i**2 - c_i**2))
    ---------------
    M = samples.grid_x*grid_y_grid_z, N = centers_p.grid_x*grid_y*grid_z
    Return: Euclidean_distance, shape: (M,N)
    '''
    samples_p_reshape = gridData_reshape(samples_p) #shape:(M,dimension)
    centers_p_reshape = gridData_reshape(centers_p) #shape:(N,dimension)
    return torch.sqrt(torch.sum((torch.unsqueeze(samples_p_reshape,1)-torch.unsqueeze(centers_p_reshape,0))**2,dim=2)) # shape: (M,N)



class SRBF_interpolation():

    def __init__(self, eps, kernel_function=Gaussian):
        '''
        ---------input---------------
        centers_p: positions of radial kernel centers, shape: ( dimension, grid_x, grid_y, grid_z)
        samples_p: positions of samples,               shape: ( dimension, grid_x, grid_y, grid_z)
        eps:       shape parameter
        kernel_function: radial kernel function
        y:         output ( dimension, grid_x, grid_y, grid_z)

        Euclidean distance: shape (M,N) where M=samples.grid_x*grid_y*grid_z, N=centers_p.grid_x*grid_y*grid_z
        phi: kernel_function(eps, Euclidean_distance); shape: (M,N)
        SRBF: b = Sum_{i}( phi(Euclidean_distance(samples_p, kernel_p_i))*weight_i )
        '''
        self.eps = eps 
        self.kernel_function = kernel_function
    def fit(self, samples_p, centers_p, samples_y):
        '''
        compute weight matrix
        -------------------
        weight: shape: (N, dimension)
        '''
        self.centers_p = centers_p
        phi = self.kernel_function(self.eps, Euclidean_distance(samples_p, centers_p)) #(M,N)
        samples_y_reshape = gridData_reshape(samples_y) #(M, dimension)
        self.weight = torch.linalg.inv(phi) @ samples_y_reshape #(N,dimension)
        self.N, self.dimension = self.weight.shape
        self.M = samples_y_reshape.shape[0]
        return self.weight 

    def __call__(self, targets_p):
        phi = self.kernel_function(self.eps, Euclidean_distance(targets_p, self.centers_p))
        return phi@self.weight

    def compute_gradient(self, targets_p, kernel_function_grad=grad_Gaussian):
        '''
        Only work for |p|**2
        --------input------------
        targets_p: shape: (1, dimension, grid_x, grid_y, grid_z)
        -------------------
        return: grad field: (M_targets, dimension(direction), dimension(component))
        '''
        # kernel_function_grad( |p|*d|p|/dx )
        grad = kernel_function_grad(self.eps, gridData_reshape(targets_p)).expand(-1, -1, self.N)

        return grad@self.weight



