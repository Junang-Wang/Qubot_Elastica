import numpy as np
from MagneticCatheterSim import *
import Sofa
import SofaRuntime
import Sofa.Gui
from tqdm import tqdm
env_stl = './SOFA_playground/mesh/qubot_flat_models/neurovascular_2D_s.stl'
USE_GUI = True
iterations = 100

def rootNodeInit():
    # Create the root node
    rootNode = Sofa.Core.Node("rootNode")
    rootNode.addObject('InteractiveCamera',name='c')
    rootNode.c.position.value = [0,0,800]
    createScene(rootNode)
    Sofa.Simulation.init(rootNode)
    return rootNode
def main():
    if not USE_GUI:
        # Create the root node
        rootNode = rootNodeInit()


        # iterate simulation step by step
        
        # Sofa.Simulation.animateNSteps(
        #     rootNode,
        #     n_steps= 100, 
        #     dt=rootNode.dt.value)

        for iteration in tqdm(range(iterations)):
            Sofa.Simulation.animate(
                rootNode,
                rootNode.dt.value
            )
        print('not using GUI')

    else:
        # Create the root node
        rootNode = rootNodeInit()
        # Launch the GUI 
        Sofa.Gui.GUIManager.Init('myscene','qt')
        Sofa.Gui.GUIManager.createGUI(rootNode,__file__)
        Sofa.Gui.GUIManager.SetDimension(1000,700)
        Sofa.Gui.GUIManager.MainLoop(rootNode)
        Sofa.Gui.GUIManager.closeGUI()

        print('GUI was closed')
    print("Simulation is done")

def createScene(rootNode):

    # Header function sets up the Animation Loop, Constraint Solver and so on.
    mcr_Header.Header(
        rootNode=rootNode, 
        gravity = [0.0, 0.0, 0.0],
        contactDistance= 1,
        alarmDistance= 2)
    
    # topoInstrument sets up the topology of instrument
    # using mm, g, s unit
    magnet_length = 40
    magnet_nbNode = 10
    magnet_remanence = 1 #mT
    radius = 1
    # magnetic field in spherical coordinate: [amplitude, polar angle, azimuth angle]
    magnetic_field_spherical = [0,np.pi/2,np.pi/2]

    Catheter = mcr_topoInstrument.Topo_Instrument(
        rootNode = rootNode,
        name   = 'Catheter',
        shapes = ['StraightSection', 'StraightSection'],
        radius = radius, 
        StraightLengths= [600, magnet_length],
        massDensity = 1550*1e-6,
        youngModulus= [10000e3, 10000e3],
        poissonRatio= [1/3, 1/3],
        nbsections  = [40, magnet_nbNode],
        nbsections_visu= [160, 40]
    )

    topo_instruments = [Catheter]
    magnet = mcr_magnetRemanence.UniformMagnet(
        length    = magnet_length,
        num_nodes = magnet_nbNode,
        remanence = magnet_remanence,
        radius    = radius
    )

    # instrumentDOFs initializes physics model, collision model, visual model and controller
    mcr_radiologyInstrumentDOFs.Instrument_DOFs(
        rootNode = rootNode,
        magnet   = magnet,
        magnetic_field_spherical = magnetic_field_spherical,
        topo_instruments = topo_instruments,
        grid_nx          = 180,
        fixed_directions = [0,0,1,0,0,0]
    )

    # environment import neurovascular tree env
    mcr_environment.environment(
        rootNode    = rootNode,
        name        = 'Env',
        filename    = env_stl,
        translation = [250.0,-470.0,-1.0],
        rotation    = [0.0,180.0,-90.0],
        scale       = 3,
        color       = [1,0,0,0.3]
    )


    return rootNode

if __name__ == '__main__':
    main()
