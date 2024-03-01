# Scalar Radial Basis Functions
import torch

def Gaussian(eps, x):
    return torch.exp(-eps*x**2)

def SRBF_interpolation(centers_p, samples_p, eps, kernel_function, y):
    '''
    centers_p: positions of radial kernel centers, shape: (num_centers, dimension)
    samples_p: positions of samples,               shape: (num_samples, dimension)
    eps:       shape parameter
    kernel_function: radial kernel function
    y:         output (num_samples)
    '''
    Euclidean_distance = torch.sum((torch.unsqueeze(samples_p,1)-torch.unsqueeze(centers_p,0))**2,dim=2) # shape: (num_samples, num_center)
    phi = kernel_function(eps, Euclidean_distance)
    weight = torch.linalg.inv(phi) @ y
    return weight 