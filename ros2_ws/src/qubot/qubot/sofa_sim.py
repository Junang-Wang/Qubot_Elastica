#! /home/qubot/.pyenv/shims/python3
import rclpy
from rclpy.node import Node
from action_interfaces.msg import MagneticSpherical 
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import threading
import numpy as np
import sys
sys.path.append('/home/qubot/ros2_ws/src/qubot/qubot')
from MagneticCatheterSim import *
import Sofa
import Sofa.Gui


class MagSubscriberNode(Node):

    def __init__(self):
        super().__init__('mag_subscriber')
        self.magnetic_field_spherical = [0.0,0.0,0.0]
        self.mag_subscriber_ = self.create_subscription(MagneticSpherical,"/controller/cmd_mag", self.mag_callback, 10)

    def mag_callback(self,msg:MagneticSpherical):
        self.get_logger().info('subscribe mag msg')
        self.get_logger().info(str(msg.magnetic_field_spherical))
        self.magnetic_field_spherical[0] = msg.magnetic_field_spherical[0]
        self.magnetic_field_spherical[1] = msg.magnetic_field_spherical[1]
        self.magnetic_field_spherical[2] = msg.magnetic_field_spherical[2]




def rootNodeInit(magnetic_field_spherical, magnet_remanence,dt, youngModulus, length, radius):
    
    # Create the root node
    rootNode = Sofa.Core.Node("rootNode")
    rootNode.addObject('Camera',name='c')
    rootNode.c.position.value = [0,0,500]
    magnetic_field_spherical = magnetic_field_spherical
    createScene(rootNode, magnetic_field_spherical=magnetic_field_spherical, magnet_remanence=magnet_remanence, dt= dt, youngModulus = youngModulus, length = length, radius=radius)
    Sofa.Simulation.init(rootNode)
    return rootNode

def main():
    youngModulus = 1.69e7
    magnet_remanence = 109.9 #mT
    length_diameter_ratio = 40
    dt = 0.001
    radius = 0.4
    length = length_diameter_ratio*radius*2 
    #---------------------------------
    # create ros2 node
    rclpy.init()
    node = MagSubscriberNode()
    task_spin = threading.Thread(target=rclpy.spin, args=(node,))
    task_spin.start()
    # rclpy.spin(node)
    
    # Create the sofa root node
    rootNode = rootNodeInit(node.magnetic_field_spherical,magnet_remanence, dt,youngModulus, length, radius)
    # Launch the GUI 
    Sofa.Gui.GUIManager.Init('myscene','qglviewer')
    Sofa.Gui.GUIManager.createGUI(rootNode,__file__)
    Sofa.Gui.GUIManager.SetDimension(1000,700)
    Sofa.Gui.GUIManager.MainLoop(rootNode)
    Sofa.Gui.GUIManager.closeGUI()
    bendingAngle = rootNode.CatheterPhysicsModel.catheterController.bendingAngle
    tangentAngle = rootNode.CatheterPhysicsModel.catheterController.tangentAngle

    # print('GUI was closed')
    # print("young's Modulus", youngModulus)
    # print('bending angles:            ', bendingAngle)
    # print('tangent angles:            ', tangentAngle)
    # print("Simulation is done")
    rclpy.shutdown()

        
def createScene(
        rootNode, 
        dt=0.01, 
        end_forces=[[0,0,0,0,0,0]],magnetic_field_spherical =[0,np.pi/2,np.pi/2], 
        magnet_remanence = 128e3*1e-3, 
        youngModulus = 1.4e6, 
        length = 6, 
        radius =0.3):

    # Header function sets up the Animation Loop, Constraint Solver and so on.
    mcr_Header.Header(
        rootNode=rootNode, 
        gravity = [0.0, 0.0, 0.0],
        contactDistance= 1,
        alarmDistance= 2,
        dt = dt)
    
    # topoInstrument sets up the topology of instrument
    # using mm, g, s unit
    magnet_length = length
    magnet_nbNode = 40
    magnet_remanence = magnet_remanence #mT
    radius = radius
    # magnetic field in spherical coordinate: [amplitude, polar angle, azimuth angle]
    magnetic_field_spherical = magnetic_field_spherical
    translations = [[0,0,0]]
    # end_forces = [[0,10,0,0,0,0]]

    Catheter = mcr_topoInstrument.Topo_Instrument(
        rootNode = rootNode,
        name   = 'Catheter',
        shapes = ['StraightSection'],
        radius = radius, 
        StraightLengths= [magnet_length],
        massDensity = 2273*1e-6,
        youngModulus= [youngModulus],
        poissonRatio= [0.5],
        nbsections  = [magnet_nbNode],
        nbsections_visu= [40]
    )

    topo_instruments = [Catheter]
    magnet = mcr_magnetRemanence.UniformMagnet(
        length        = magnet_length,
        num_nodes     = magnet_nbNode,
        remanence     = magnet_remanence,
        radius        = radius
    )

    # instrumentDOFs initializes physics model, collision model, visual model and controller
    mcr_fixedInstrumentDOFs.Instrument_DOFs(
        rootNode = rootNode,
        magnet   = magnet,
        magnetic_field_spherical = magnetic_field_spherical,
        end_forces = end_forces,
        topo_instruments = topo_instruments,
        translations     = translations,
        fixed_directions = [0,0,1,0,0,0]
    )



    return rootNode

    

if __name__ =='__main__':
    main()