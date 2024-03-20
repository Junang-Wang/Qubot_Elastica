import numpy as np
from scipy.spatial.transform import Rotation as R
import Sofa
class catheterController(Sofa.Core.Controller):
    '''
    Controller 
    PhysicsModel  : PhysicsModel applied controlled
    magnets_num_nodes : number of magnet nodes 
    dipole_moment_amp : dipole moment amplitude of one section
    magnetic_field_spherical : external magnetic field in spherical coordinate

    '''
    def __init__(self,
                 PhysicsModel,
                 magnets,magnetic_field_spherical,
                 *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.PhysicsModel = PhysicsModel
        self.magnets_num_nodes = magnets.num_nodes
        self.dipole_moment_amp = magnets.dipole_moment_amp
        self.magnetic_field_spherical = magnetic_field_spherical
    
    def onKeypressedEvent(self,event):
        ConstantForce = self.PhysicsModel.CollectorEndForceField.forces[0][0:2]
        amplitude = np.linalg.norm(ConstantForce)
        # print(ConstantForce)
        theta = np.angle(complex(*ConstantForce))
        key = event['key']
        if key == ']':
            theta += 2*np.pi/36
            print('increasing theta')
        elif key == '[':
            theta -= 2*np.pi/36
            print('reducing theta')
        elif key == '=':
            amplitude += 1e2 #mu_N
            print('adding forces')
        elif key == "-":
            amplitude -= 1e2
            print('reducing forces')
        elif key == '0':
            self.magnetic_field_spherical[2] += 2*np.pi/20
            print('increasing magnetic azimuth angle')
        elif key == '9':
            self.magnetic_field_spherical[2] -= 2*np.pi/20
            print('decreasing magnetic azimuth angle')
        elif key == '8':
            self.magnetic_field_spherical[0] += 1e1 #mT
            print('Adding magnetic amplitude')
        elif key == '7':
            if self.magnetic_field_spherical[0]<=0:
                pass
            else:
                self.magnetic_field_spherical[0] -= 1e1
            print('Reducing magnetic amplitude')
        self.PhysicsModel.CollectorEndForceField.forces[0][:2] = [np.cos(theta)*amplitude, np.sin(theta)*amplitude]


    def onAnimateBeginEvent(self, event):
        '''
        Apply responding torque on magnetic nodes given a magnetic field and the pose of the node
        '''
        mag_pos = np.array(self.PhysicsModel.Instrument_DOFs.position[-self.magnets_num_nodes:])
        quaternions = mag_pos[:,3:]
        # convert quaternions to rotation matrix
        r = R.from_quat(quaternions)
        x = np.array([1,0,0])
        # compute dipole moment direction
        dipole_moment_dir = r.apply(np.tile(x,(self.magnets_num_nodes,1)))

        # store bending angle
        self.bendingAngle = np.arctan2(mag_pos[-1,1],mag_pos[-1,0])/np.pi * 180
        # store end point tangent line Angle
        self.tangentAngle = np.arctan2(dipole_moment_dir[-1][1],dipole_moment_dir[-1][0])/np.pi * 180
        # store end of catheter position
        self.endPosition = mag_pos[-1,0:3]

        forces = np.tile(np.zeros(6), (self.magnets_num_nodes,1))
        magnetic_field_visu = np.tile(np.zeros(6), (1,1))
        # compute magnetic torque
        magnetic_field = self.magnetic_field_spherical[0]*np.array([np.sin(self.magnetic_field_spherical[1])*np.cos(self.magnetic_field_spherical[2]),np.sin(self.magnetic_field_spherical[1])*np.sin(self.magnetic_field_spherical[2]), np.cos(self.magnetic_field_spherical[1])])
        # print('dipole', dipole_moment_dir)
        # print(self.dipole_moment_amp*np.cross(dipole_moment_dir,magnetic_field))
        forces[:,3:] = self.dipole_moment_amp*np.cross(dipole_moment_dir,magnetic_field)
        # apply torque
        self.PhysicsModel.CollectorMagneticForceField.forces = forces.tolist()
        magnetic_field_visu[:,:3] = magnetic_field
        # apply magnetic field visualization
        self.PhysicsModel.MagneticFieldVisual.forces = magnetic_field_visu.tolist()
        # print(magnetic_field_visu.tolist())
        # print('forces:',self.PhysicsModel.CollectorMagneticForceField.forces[:])
        self.PhysicsModel.VisualCatheter.VisuOgl.OglLabel.label =f'{self.magnetic_field_spherical[0]:.0f} mT'