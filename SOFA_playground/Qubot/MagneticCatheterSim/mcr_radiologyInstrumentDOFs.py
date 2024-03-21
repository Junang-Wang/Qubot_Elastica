import numpy as np
from MagneticCatheterSim.mcr_controller import catheterController
def Instrument_DOFs(
        rootNode,
        magnet,
        magnetic_field_spherical,
        topo_instruments,
        grid_nx,
        fixed_directions = [0,0,1,0,0,0]
):
    '''
    This function initializes physics model and visual model of instruments
    magnet                   : magnet class which attach to the tip of instruments
    magnetic_field_spherical : applied magnetic field in spherical coordinate
    topo_instruments         : topology information of instruments
    grid_nx                  : number of grid edges
    fixed_directions         : the constrained direction, 1 for constrained, the first three refer to the translation along x,y,z. The last three represent the rotation(torque) around x,y,z 
    '''
    # mechanical model of Catheter
    PhysicsModel = rootNode.addChild('PhysicsModel')
    
    PhysicsModel.addObject(
        'EulerImplicitSolver', 
        rayleighStiffness=0.2, 
        printLog=False, 
        rayleighMass=0.1)
    PhysicsModel.addObject(
        'BTDLinearSolver', 
        subpartSolve = False,
        verification = False, 
        verbose=False)
    PhysicsModel.addObject(
        'RegularGridTopology',
        name='MeshLines', 
        drawEdges=False, 
        nx=grid_nx, ny=1, nz=1,
        xmax=0, xmin=0.0, ymin=0, ymax=0, zmax=0, zmin=0,
        p0=[0,0,0])
    PhysicsModel.addObject(
        'MechanicalObject', 
        showIndices=False, 
        name='Instrument_DOFs', 
        template='Rigid3d')
    # FEM method (BeamInterpolation)
    # plug the catheter RestShape into WireBeamInterpolation 
    BeamInterpolationName = []
    for i in range(len(topo_instruments)):
        PhysicsModel.addObject(
            'WireBeamInterpolation', 
            name='Interpol'+topo_instruments[i].name, 
            WireRestShape='@../'+topo_instruments[i].name + '/' + topo_instruments[i].WireRestShapeName, 
            radius=topo_instruments[i].radius, printLog=False)
        BeamInterpolationName.append('Interpol'+topo_instruments[i].name)  
    # compute internal forces
    # computeMass if false, only compute the stiff elastic model
    # massDensity: Density of the mass
    # shearStressComputation: if false, suppress the shear stress in the computation
    # reinforceLength: a separation computation for the error in elongation is performed
        PhysicsModel.addObject(
            'AdaptiveBeamForceFieldAndMass', 
            name=topo_instruments[i].name+'BeamForceField', massDensity=topo_instruments[i].massDensity, interpolation='@Interpol'+topo_instruments[i].name, 
            computeMass=True, 
            reinforceLength= False, 
            shearStressComputation= False)
    # Constant Force Field
    PhysicsModel.addObject(
        'ConstantForceField', 
        name='CollectorEndForceField', 
        indices=0, 
        forces=[0,0,0,0,0,0],
        indexFromEnd=True, 
        showArrowSize=1e-2)
    PhysicsModel.addObject(
        'ConstantForceField', 
        name='CollectorMagneticForceField', 
        indices=np.arange(topo_instruments[0].nbsections[-1]), 
        forces=np.tile(np.zeros(6)+100, (topo_instruments[0].nbsections[-1],1)),
        indexFromEnd=True, 
        showArrowSize=1e-2,
        showColor=[1,0,0,1])
    PhysicsModel.addObject(
        'ConstantForceField', 
        name='MagneticFieldVisual', 
        indices=0, 
        forces=[0,0,0,0,0,0], 
        showArrowSize=1e-1)

    PhysicsModel.addObject(
        catheterController(
            PhysicsModel,magnet, 
            magnetic_field_spherical,
            name='catheterController'))
    #Deployment Controller
    PhysicsModel.addObject(
        'InterventionalRadiologyController', 
        name='DeployController', 
        template='Rigid3d', 
        instruments=' '.join(BeamInterpolationName), 
        startingPos=[0,0,0,0,0,0,1], 
        xtip=1, 
        printLog=False, 
        rotationInstrument=[0, 0, 0], 
        step=3, 
        speed=4, 
        listening=True, 
        controlledInstrument=0)
    PhysicsModel.addObject(
        'LinearSolverConstraintCorrection', wire_optimization=True)

    PhysicsModel.addObject(
        'FixedConstraint', 
        indices=0, 
        name='FixedConstraint')
    # Add constraint box
    # box = [0,0,-50,120,6,70]
    # PhysicsModel.addObject('BoxROI',name='BoxROI',box = box, drawBoxes=True, doUpdate=False)
    PhysicsModel.addObject(
        'RestShapeSpringsForceField', 
        name="RestSPForceField", 
        points='@DeployController.indexFirstNode', 
        angularStiffness=1e8, 
        stiffness=1e8)
    PhysicsModel.addObject(
        'PartialFixedConstraint', 
        fixedDirections = fixed_directions,
        indices=np.arange(grid_nx))
        #-----------------------------------------------------------------------
    # Collision model
    Collis = PhysicsModel.addChild('CollisionCatheter')
    Collis.activated = True
    Collis.addObject(
        'MechanicalObject', 
        name='colli_DOFs',
        template='Vec3d')
    # if use 1D line mesh, one can extend to 2D surf mesh
    # if one needs 3D mesh, one has to import stl 3D files or deploys CylinderGridTopology

    # CollisionCatheter.addObject('QuadSetTopologyContainer',name = 'colli_container')
    # CollisionCatheter.addObject('QuadSetTopologyModifier')
    # CollisionCatheter.addObject('QuadSetGeometryAlgorithms',showPointIndices=False, showEdgeIndices=False, drawEdges=False)
    # CollisionCatheter.addObject('Edge2QuadTopologicalMapping',nbPointsOnEachCircle=10,
    #                             radius=radius, input='@../../GuideCatheter/meshLinesBeam',
    #                             output='@colli_container')

    # CollisionCatheter.activated = True
    Collis.addObject('EdgeSetTopologyContainer',name='collisEdgeSet')
    Collis.addObject('EdgeSetTopologyModifier',name='colliseEdgeModifier')

    # CylinderGridTopology, nz is the longitudinal direction discretization
    # CollisionCatheter.addObject('CylinderGridTopology', name ='Cylinder_container', axis= [1,0,0], center = [0,0,0], length=length, radius=radius, nx=5, ny=5, nz=6)
    Collis.addObject(
        'MultiAdaptiveBeamMapping',
        controller='../DeployController',
        useCurvAbs=True, 
        printLog=False,
        name='collisMap')
    Collis.addObject('PointCollisionModel',proximity=0.0)
    Collis.addObject('LineCollisionModel', proximity=0.0)
    # CollisionCatheter.addObject('TriangleCollisionModel')
    # CollisionCatheter.addObject('TetrahedronCollisionModel')

        #--------------------------------------------------------------------
    # Visual model: using WireRestShape mesh
    for i in range(len(topo_instruments)):
        VisualInstrument = PhysicsModel.addChild('Visual'+topo_instruments[i].name)
        
        VisualInstrument.addObject(
            'MechanicalObject', 
            name= 'visu_DOFs',
            template='Vec3d')
        
        VisualInstrument.addObject(
            'QuadSetTopologyContainer', 
            name = "visu_container")
        VisualInstrument.addObject('QuadSetTopologyModifier')
        VisualInstrument.addObject('QuadSetGeometryAlgorithms')
        # Mapping WireRestShape mesh to topology container
        VisualInstrument.addObject(
            'Edge2QuadTopologicalMapping', 
            nbPointsOnEachCircle=10,
            radius=topo_instruments[i].radius, 
            input=f'@../../{topo_instruments[i].name}/meshLinesBeam', output='@visu_container')
        # Mapping mesh to Beam Mechanics
        VisualInstrument.addObject(
            'AdaptiveBeamMapping', 
            input="@../Instrument_DOFs", 
            output="@visu_DOFs", 
            interpolation=f'@../Interpol{topo_instruments[i].name}')
        
        # Visual beam by OglModel
        VisuOgl = VisualInstrument.addChild('VisuOgl')
        VisuOgl.addObject(
            "OglModel", 
            name="visual", 
            color=[0.5,1,0.5], 
            quads="@../visu_container.quads")
        VisuOgl.addObject(
            'IdentityMapping', 
            input="@../visu_DOFs",
            output='@visual')
    VisuOgl.addObject(
        'OglLabel',
        label=f'{PhysicsModel.catheterController.magnetic_field_spherical[0]:.0f} mT',
        x=0, y=0, 
        fontsize=50, 
        updateLabelEveryNbSteps=1,
        selectContrastingColor=True)