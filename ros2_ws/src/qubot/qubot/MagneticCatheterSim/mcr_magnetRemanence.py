import numpy as np
class UniformMagnet():
    def __init__(
            self, 
            length, 
            num_nodes, 
            remanence, 
            radius,
            inner_radius = 0,
            magnetPercent = 1,
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
        self.remanence = remanence
        self.radius = radius 
        self.inner_radius = inner_radius
        self.color = color
        self.num_nodes = num_nodes

        # mu_0 permeability of vacuum: 4*pi*10^-7 * 10^6 mT*mT*mm*s^2/g
        self.mu_0 = (4.*np.pi)*1e-1
        self.volume = magnetPercent*self.length * np.pi * (self.radius**2 - self.inner_radius**2) 

        # dipole moment: 1/mu_0* remanence * Volume nJ/mT = muN*mm/mT
        self.dipole_moment_amp = (1./self.mu_0)*self.remanence*self.volume
        self.magnetization = (1./self.mu_0)*self.remanence