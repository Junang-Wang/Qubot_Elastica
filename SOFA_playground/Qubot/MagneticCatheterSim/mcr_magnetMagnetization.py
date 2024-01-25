import numpy as np
class UniformMagnet():
    def __init__(
            self, 
            length, 
            num_nodes, 
            magnetization, 
            radius,
            inner_radius = 0,
            color = [0.2,0.2,0.2,1]):
        '''
        Magnet class indicate magnetic material uniformly distributed
        length    : length of magnet
        num_nodes : number of catheter nodes applied magnet
        remanence : magnet remanence
        radius    : magnet radius
        inner_radius: magnet inner radius 
        '''
        # mmGS unit
        # uniform distribution remanence
        self.length = length/num_nodes #mm
        self.magnetization = magnetization 
        self.radius = radius 
        self.inner_radius = inner_radius
        self.color = color
        self.num_nodes = num_nodes

        self.volume = self.length * np.pi * (self.radius**2 - self.inner_radius**2) 

        # dipole moment: 1/mu_0* remanence * Volume nJ/mT = muN*mm/mT
        self.dipole_moment_amp = self.magnetization*self.volume