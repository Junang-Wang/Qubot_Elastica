import numpy as np
from MagneticCatheterSim import *
import Sofa
import SofaRuntime
import Sofa.Gui
from tqdm import tqdm
from utils import plotMagneticFigure
USE_GUI = False

def rootNodeInit(magnetic_field_amplitudes, dt, youngModulus, length, radius):
    # Create the root node
    rootNode = Sofa.Core.Node("rootNode")
    rootNode.addObject('Camera',name='c')
    rootNode.c.position.value = [0,0,500]
    magnetic_field_spherical = [magnetic_field_amplitudes,np.pi/2, np.pi/2]
    createScene(rootNode, magnetic_field_spherical=magnetic_field_spherical, dt= dt, youngModulus = youngModulus, length = length, radius=radius)
    Sofa.Simulation.init(rootNode)
    return rootNode

def main():
    youngModulus = 1.4e6
    # number of samples of magnetic field amplitude
    m_size = 30
    # number of samples length diameter ratio 
    r_size = 3
    microscope_size = 10
    small_scope_size =10
    magnetic_field_amplitudes =np.concatenate(
         (np.linspace(0,1,small_scope_size,endpoint=False),np.linspace(1,10,small_scope_size,endpoint=False),np.linspace(10,100,m_size-small_scope_size-microscope_size)),axis=0) #mT
    magnet_magnetization = 128e3*1e-3
    length_diameter_ratio = np.linspace(10,20,r_size)
    delta_div_L = np.zeros((r_size,m_size))
    tangentAngle = np.zeros_like(delta_div_L)
    bendingAngle = np.zeros_like(delta_div_L)
    dt = 0.001
    time = 2
    radius = 0.3
    length = length_diameter_ratio*radius*2 


    iterations = int(time/dt)
    if not USE_GUI:
        for i in range(r_size):
            for j in range(m_size):
                # Create the root node
                rootNode = rootNodeInit(magnetic_field_amplitudes[j],dt, youngModulus, length[i], radius)

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
                delta_div_L[i,j] = rootNode.CatheterPhysicsModel.catheterController.endPosition[1]/length[i]
            print('not using GUI')
        plotMagneticFigure(magnetic_field_amplitudes, magnet_magnetization, youngModulus, r_size, tangentAngle, length_diameter_ratio, small_scope_size, delta_div_L)
    else:
        # Create the root node
        rootNode = rootNodeInit(magnetic_field_amplitudes[28],dt,youngModulus, length[0], radius)
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
    print('magnetic field amplitude', magnetic_field_amplitudes)
    print('bending angles:            ', bendingAngle)
    print('tangent angles:            ', tangentAngle)
    print("Simulation is done")

        
def createScene(
        rootNode, 
        dt=0.01, 
        end_forces=[[0,0,0,0,0,0]],magnetic_field_spherical =[0,np.pi/2,np.pi/2], 
        magnet_magnetization = 128e3*1e-3, 
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
    magnet_magnetization = magnet_magnetization #A/mm
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
    magnet = mcr_magnetMagnetization.UniformMagnet(
        length        = magnet_length,
        num_nodes     = magnet_nbNode,
        magnetization = magnet_magnetization,
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

if __name__ == '__main__':
    main()