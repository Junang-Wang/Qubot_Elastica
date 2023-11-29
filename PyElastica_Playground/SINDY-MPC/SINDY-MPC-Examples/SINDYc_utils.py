import numpy as np
from scipy import integrate
import cvxpy as cp
import time
def poolData(xin,polyorder,usesine):
    """
    This function compute the polynomial of x, output the Theta in SINDYc 
    xin: input variable of dynamics
    polyorder: the maximum order of polynomial 
    usesine: Whether using sine and cosine to construct Theta
    """
# For Paper, "Discovering Governing Equations from Data: 
#        Sparse Identification of Nonlinear Dynamical Systems"
# by S. L. Brunton, J. L. Proctor, and J. N. Kutz
    time_size, n = xin.shape 
    origin = np.ones((time_size,1))
    poly_x = origin
    xout = np.ones((time_size,int((1-n**(polyorder+1))/(1-n))) )
    old_ind = 0
    for i in range(polyorder):
        poly_x = (np.einsum('ij,ik->ijk',xin,poly_x)).reshape(time_size,n**(i+1)) # the vector of all product combinations of the components in x and factors
        new_ind = old_ind + n**(i+1)
        xout[:,old_ind+1:new_ind+1] = poly_x
        old_ind = new_ind


    if usesine:
        for k in range(1,11):
            xout = np.concatenate((xout, np.sin(k*xin), np.cos(k*xin)),axis=1)
    
    return xout

def poolData_cvxpy(xin,polyorder,usesine):
    """
    This function compute the polynomial of x, output the Theta in SINDYc for cvxpy opt
    xin: input variable of dynamics 1D array
    polyorder: the maximum order of polynomial 
    usesine: Whether using sine and cosine to construct Theta
    """
    origin = np.ones(1)
    factors = origin
    xout = np.ones(1)
    for i in range(polyorder):
        poly_x = cp.vec( cp.outer(xin,factors)) # the vector of all product combinations of the components in x and factors
        xout = cp.hstack([xout, poly_x])
        factors = poly_x


    if usesine:
        for k in range(1,11):
            xout = cp.hstack([xout, np.sin(k*xin), np.cos(k*xin)])
    
    return xout


def sparsifyDynamics(Theta,dx,Lambda,n):
    """
    This function computes Xi from the equation dx = Theta@ Xi by using Sequentially thresholded least squares algorithm 
    Lambda: the threshold
    n: dimension of [x,u]
    """
# For Paper, "Discovering Governing Equations from Data: 
#        Sparse Identification of Nonlinear Dynamical Systems"
# by S. L. Brunton, J. L. Proctor, and J. N. Kutz

# compute Sparse regression: sequential least squares
    Xi =  np.linalg.pinv(Theta)@dx  # initial guess: Least-squares

# lambda is our sparsification knob.
    for _ in range(10):
        smallinds = (abs(Xi)<Lambda)   # find small coefficients
        Xi[smallinds]=0                # and threshold
        for ind in range(n):                   # n is state dimension
            biginds = ~smallinds[:,ind]
            # Regress dynamics onto remaining terms to find sparse Xi
            Xi[biginds,ind] =  np.linalg.pinv(Theta[:,biginds]) @ dx[:,ind]
    return Xi

def sparseGalerkinControl(t,x,forcing,Xi,polyorder,usesine):
    '''
    This function computes dx by dx = Theta@Xi, where Theta is constructed by collected data
    '''
    u = forcing(x,t)
    xPool = poolData(np.concatenate((x.reshape(1,-1),u.reshape(1,-1)),axis=1),polyorder,usesine)
    dx = (xPool@Xi).reshape(-1)
    return dx

def sparseGalerkinControl_discrete(t,x,u,p,cvxpy):
    '''
    This function computes dx by dx = Theta@Xi, where Theta is constructed by collected data where forcing is stored in u
    only focus on dx instead du
    Input:     
    x: 1D array
    u: 1D array
    '''
    polyorder, usesine, Xi = p 
    if cvxpy:
        xPool = poolData_cvxpy(cp.hstack((x, u)), polyorder, usesine)
        dx = cp.vec(xPool@Xi[:,:-1])
    else:
        xPool = poolData(np.concatenate((x.reshape(1,-1),u.reshape(1,-1)),axis=1),polyorder,usesine)
        dx = (xPool@Xi[:,:-1]).reshape(-1)
    return dx

def lotkaObjectiveFCN(u,xk,Ts,N,xref,u0,p,Q,R,Ru):
    ## Cost function of nonlinear MPC for Lotka-Volterra system
    #
    # Inputs:
    #   u:      optimization variable, from time k to time k+N-1 
    #   xk:      current state at time k
    #   Ts:     controller sample time
    #   N:      prediction horizon
    #   xref:   state references, constant from time k+1 to k+N
    #   u0:     previous controller output at time k-1
    #   p:      variable library parameters (tuple) 
    #   Q:      State weights
    #   R:      Control variation du weights
    #   Ru      Control u weights
    #
    # Output:
    #   J:      objective function cost
    #

    ## Nonlinear MPC design parameters


    ## Cost Calculation
    # Set initial plant states, controller output and cost
    #polyorder, usesine, Xi = p 
    J = 0
    
    # Loop through each prediction step
    for i in range(N):
        uk = u[i]
        # Obtain plant state at next prediction step
        xk = rk4u(sparseGalerkinControl_discrete,xk,uk,Ts,1,[],p,cvxpy=False)
        
        J += ((xk-xref).T)@Q@(xk-xref) 
    delta_u = u - np.insert(u[:-1],0,u0)
    J +=  (delta_u.T)@np.kron(np.eye(N),R)@delta_u + u.T@np.kron(np.eye(N),Ru)@u
    
    return J

def lotkaObjectConstraint_cvxpy(uu,xx,delta_u,u0,x0,xref,weights,Ts,p):
    N = uu.shape[0]
    J = 0.0
    Constraints = []
    Q,R,Ru = weights
    for i in range(N):
        uk = uu[i]
        
        if i == 0:
            Constraints += [delta_u[i] == uu[i] - u0] 
            Constraints += [xx[i] == rk4u(sparseGalerkinControl_discrete,x0,uk,Ts,1,[],p,cvxpy=True)]
            
        else:
            Constraints += [delta_u[i] == uu[i] - uu[i-1]] 
            Constraints += [xx[i] == rk4u(sparseGalerkinControl_discrete,xx[i-1],uk,Ts,1,[],p,cvxpy=True)]
        J += cp.quad_form(xx[i]-xref, Q) 
    prob = cp.Problem(cp.Minimize(J), constraints=Constraints)
    prob.solve()
    return uu.value,xx.value,delta_u.value
#------------discrete integration--------
def rk4u(func,x,u,h,n,t,p,cvxpy=False):
    '''
    Discrete integration RK4U: 
    Input
    ----------------------
    func: dynamics function return dx
    x:    current state
    u:    current control
    h:    time-step
    n:    number of time-steps
    t:    time
    p:    SINDYc parameters
    cvxpy: using cvxpy or not
    ---------------------
    Output:
    next step state x
    '''
    

    # RK4U   Runge-Kutta scheme of order 4 for control system
    #   rk4u(v,X,U,h,n) performs n steps of the scheme for the vector field v
    #   using stepsize h on each row of the matrix X
    #
    #   v(X,U) maps an (m x d)-matrix X and an (m x p)-matrix U
    #          to an (m x d)-matrix 
    for i in range(n):
        k1 = func(t,x,u,p,cvxpy); 
        k2 = func(t,x + h/2*k1,u,p,cvxpy)
        k3 = func(t,x + h/2*k2,u,p,cvxpy)
        k4 = func(t,x + h*k3,u,p,cvxpy)
        x = x + h*(k1 + 2*k2 + 2*k3 + k4)/6
        # x = x + h*k1
    return x