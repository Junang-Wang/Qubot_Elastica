import numpy as np
from MagneticCatheterSim import *
import Sofa
import SofaRuntime
import Sofa.Gui
from tqdm import tqdm
from utils import plotMagneticFigurePKU
USE_GUI = False

def rootNodeInit(
        magnetic_field_amplitudes,
        pAngles,
        magnet_remanence,
        magnetPercent,
        dt, 
        youngModulus, 
        length, 
        radius):
    # Create the root node
    rootNode = Sofa.Core.Node("rootNode")
    rootNode.addObject('Camera',name='c')
    rootNode.c.position.value = [0,0,500]
    magnetic_field_spherical = [magnetic_field_amplitudes,np.pi/2, pAngles]
    createScene(
        rootNode, magnetic_field_spherical=magnetic_field_spherical,
        dt= dt, 
        youngModulus = youngModulus, 
        length = length, 
        radius=radius, 
        magnet_remanence=magnet_remanence,
        magnetPercent= magnetPercent)
    Sofa.Simulation.init(rootNode)
    return rootNode

def main():
    magnet_remanence = 109.9 #mT
    mu_0 = (4.*np.pi)*1e-1 # permeability of vacuum
    magnet_magnetization = 1./mu_0*magnet_remanence
    magnetPercent = 1
    MG_ratio = 1.9526e-5 #mT/Pa
    youngModulus = magnet_remanence / MG_ratio * 3


    small_scope_size =10
    magnetic_field_amplitudes = np.array([
        [0.0 ,14.0,28.0,45.0,60.0,73.0,85.0,100.0,115.0, 144.0],#30 deg
        [11.0,25.5,44.0,52.0,70.0,86.0,100.0,113.5,127.0,144.0],#60 deg
        [10.0,25.0,40.0,58.0,72.0,85.0,100.5,113.0,127.5,140.0],#90 deg 
        [17.0,26.5,44.5,57.0,70.0,84.0,100.0,114.0,128.0,144.0],#90 deg
        [12.0,25.0,40.0,54.0,69.5,81.0,97.0,111.5,128.0, 138.0],#120 
        [12.5,24.0,37.5,53.5,67.5,79.0,95.0,108.5,125.5, 138.5],#150
    ])
    # magnetic_field_amplitudes = np.array([
    #     [12.5,24.0,37.5,53.5,67.5,79.0,95.0,108.5,125.5, 138.5],#150
    # ])
    # experimentBendingAngles = np.array([
    #     [32.144903,54.215262,73.146556,87.446083,96.027373,100.480425,106.337402,109.552638,113.341916,115.765885]
    # ])
    experimentBendingAngles = np.array([
        [0.0,      8.338849,13.468069,17.005383,18.613571,19.730294,20.377006,21.149582,22.119853,22.679185],
        [14.526040,28.329948,35.148414,37.094230,40.065504,42.174558,42.968182,44.931512,45.776669,46.429566],
        [21.869741,39.612258,50.604539,57.219379,60.953746,64.006820,66.582632,67.640306,68.867246,70.049643],
        [29.293433,40.348314,51.033602,59.400021,62.292449,64.107996,66.095956,68.375211,69.376469,70.398417],
        [29.450856,48.891132,65.134193,71.694862,78.844496,82.420128,86.338957,89.427026,93.680150,94.265264],
        [32.144903,54.215262,73.146556,87.446083,96.027373,100.480425,106.337402,109.552638,113.341916,115.765885],
    ])
    # number of samples position configuration 
    p_size = magnetic_field_amplitudes.shape[0]
    # number of samples of magnetic field amplitude
    m_size = magnetic_field_amplitudes.shape[1]
    pAngles = [np.pi/6, np.pi/3, np.pi/2, np.pi/2, 2*np.pi/3, 5*np.pi/6]


    delta_div_L = np.zeros((p_size,m_size))
    tangentAngle = np.zeros_like(delta_div_L)
    bendingAngle = np.zeros_like(delta_div_L)
    dt = 0.001
    time = 2
    radius = 0.4
    length = 32 


    iterations = int(time/dt)
    if not USE_GUI:
        for i in range(p_size):
            for j in range(m_size):
                # Create the root node
                rootNode = rootNodeInit(
                            magnetic_field_amplitudes[i,j],
                            pAngles[i],
                            magnet_remanence, 
                            magnetPercent,
                            dt,
                            youngModulus, 
                            length, 
                            radius)

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
                delta_div_L[i,j] = rootNode.CatheterPhysicsModel.catheterController.endPosition[1]/length
            print('not using GUI')
        plotMagneticFigurePKU(
            magnetic_field_amplitudes, 
            magnet_magnetization, 
            youngModulus, 
            p_size, 
            bendingAngle,
            experimentBendingAngles,
            pAngles,
            small_scope_size, 
            delta_div_L)
    else:
        # Create the root node
        rootNode = rootNodeInit(
            magnetic_field_amplitudes[2,2],
            pAngles[2],
            magnet_remanence, 
            magnetPercent,
            dt,
            youngModulus, 
            length, 
            radius)
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
        magnet_remanence = 1, 
        magnetPercent = 1,
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
    magnet_remanence = magnet_remanence #A/mm
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
        massDensity = 2043*1e-6,
        youngModulus= [youngModulus],
        poissonRatio= [0.5],
        nbsections  = [magnet_nbNode],
        nbsections_visu= [40]
    )

    topo_instruments = [Catheter]
    magnet = mcr_magnetRemanence.UniformMagnet(
        length       = magnet_length,
        num_nodes    = magnet_nbNode,
        remanence    = magnet_remanence,
        magnetPercent= magnetPercent,
        radius       = radius
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