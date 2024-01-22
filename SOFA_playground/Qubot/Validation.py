import numpy as np
from MagneticCatheterSim import *
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
    translations = [[0,0,0]]
    end_forces = [[0,10,0,0,0,0]]

    Catheter = mcr_topoInstrument.Topo_Instrument(
        rootNode = rootNode,
        name   = 'Catheter',
        shapes = ['StraightSection'],
        radius = radius, 
        StraightLengths= [magnet_length],
        massDensity = 1550*1e-6,
        youngModulus= [10000e3],
        poissonRatio= [1/3],
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