import numpy as np
class lotkacontrol_class:

    def __init__(self,foring,a,b,d,g):
        self.foring = foring 
        self.a = a
        self.b = b
        self.d = d 
        self.g = g 
    
    def compute_dynamics(self,t,y):
        u = self.foring(0,t)
        dy = np.zeros(2)
        dy[0] = self.a * y[0] - self.b*y[0]*y[1]
        # print('a',self.a, 'b', self.b,'y0',y[0],'y1',y[1])
        dy[1] = self.d*y[0]*y[1] - self.g*y[1] + u
        return dy

    @staticmethod 
    def lotka_func(u,a,b,d,g):
        return lotkacontrol_class(u,a,b,d,g).compute_dynamics

def lotkacontrol(t,y,forcing,a,b,d,g):
    """
    Ground true dynamics of lotkac
    """
    u = forcing(0,t)
    dy = np.zeros(2)
    dy[0] = a * y[0] - b*y[0]*y[1]
    dy[1] = d*y[0]*y[1] - g*y[1] + u
    return dy


def lotacontrol_jac(t,y,u,a,b,d,g):
    """
    Jacobian of Ground true lotkac dynamics
    """
    # Jacobian
    J = np.zeros([2,2])
    J[0,0] = a - b*y[1] 
    J[0,1] = -b*y[0]
    J[1,0] = d*y[1] 
    J[1,1] = d*y[0] - g
    return J

def lotkacontrol_discrete(t,y,uk,p,cvxpy):
    """
    Ground true dynamics of lotkac
    """
    a, b, d, g = p
    dy = np.zeros(2)
    dy[0] = a * y[0] - b*y[0]*y[1]
    dy[1] = d*y[0]*y[1] - g*y[1] + uk
    return dy
