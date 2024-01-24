import numpy as np
from MagneticCatheterSim import *
import Sofa
import SofaRuntime
import Sofa.Gui
from tqdm import tqdm
from utils import plotFigure
USE_GUI = False

def rootNodeInit(magnetic_field_amplitude, dt, youngModulus, length, radius):
    # Create the root node
    rootNode = Sofa.Core.Node("rootNode")
    rootNode.addObject('Camera',name='c')
    rootNode.c.position.value = [0,0,500]
    magnetic_field_spherical = [magnetic_field_amplitude,np.pi/2, np.pi/2]
    createScene(rootNode, magnetic_field_spherical=magnetic_field_spherical, dt= dt, youngModulus = youngModulus, length = length, radius=radius)
    Sofa.Simulation.init(rootNode)
    return rootNode

def main():
    youngModulus = [1.4e6,14e6]
    forces = np.concatenate((np.linspace(1e-5,2e-3,6),np.linspace(2e-3,0.02,10)))*1e6 
    dt = 0.001
    time = 2
    loops = forces.size
    length = 6 # constant
    radius = 0.3
    analyticalBendingAngle = np.zeros((len(youngModulus),loops))
    bendingAngle = np.zeros((len(youngModulus),loops))
    tangentAngle = np.zeros((len(youngModulus),loops))

    iterations = int(time/dt)
    if not USE_GUI:
        for i in range(len(youngModulus)):
            for j in range(loops):
                # Create the root node
                rootNode = rootNodeInit(forces[j],dt, youngModulus[i],length, radius)
                analyticalBendingAngle[i] = np.arctan(4*forces*length**2/(3*youngModulus[i]*radius**4*np.pi))/np.pi*180

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
                bendingAngle[i,j] = rootNode.CatheterPhysicsModel.catheterController.bendingAngle
                tangentAngle[i,j] = rootNode.CatheterPhysicsModel.catheterController.tangentAngle
            print('not using GUI')
        plotFigure(forces,analyticalBendingAngle,bendingAngle)
    else:
        # Create the root node
        rootNode = rootNodeInit(forces[1],dt,youngModulus[0], length, radius)
        # Launch the GUI 
        Sofa.Gui.GUIManager.Init('myscene','qglviewer')
        Sofa.Gui.GUIManager.createGUI(rootNode,__file__)
        Sofa.Gui.GUIManager.SetDimension(1000,700)
        Sofa.Gui.GUIManager.MainLoop(rootNode)
        Sofa.Gui.GUIManager.closeGUI()
        bendingAngle[0,0] = rootNode.CatheterPhysicsModel.catheterController.bendingAngle
        tangentAngle[0,0] = rootNode.CatheterPhysicsModel.catheterController.tangentAngle

        print('GUI was closed')
    print("young's Modulus", youngModulus)
    print('magnetic field amplitude', magnetic_field_spherical)
    print('analytical bending angles: ', analyticalBendingAngle)
    print('bending angles:            ', bendingAngle)
    print('tangent angles:            ', tangentAngle)
    print("Simulation is done")

        
def createScene(rootNode, dt=0.01, end_forces=[[0,0,0,0,0,0]],magnetic_field_spherical =[0,np.pi/2,np.pi/2], magnet_remanence = 1, youngModulus = 1.4e6, length = 6, radius =0.3):

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
    magnet = mcr_magnet.UniformMagnet(
        length    = magnet_length,
        num_nodes = magnet_nbNode,
        remanence = magnet_remanence,
        radius    = radius
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

if __name__ == '__main__':
    main()