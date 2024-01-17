# This file adds collision model into the actuator and add a env. Meanwhile constrains catheter to 2D.
# now Catheter contains two sections, one is stiff and the other is softer. The parameters of Catheter 
# use SOFA example parameters. In the unit of mm, g
# Author: JunAng Wang
# Contact: wangjunang94@gmail.com
from stlib3.scene import MainHeader
from plugin_list import pluginList, display
import numpy as np
def createScene(rootNode):

    # Header
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('DefaultVisualManagerLoop')
    rootNode.addObject('LCPConstraintSolver',mu=0.1,tolerance=1e-4,maxIt=1000,build_lcp=False)
    rootNode.addObject('CollisionPipeline',draw=0,depth=6,verbose='1')
    rootNode.addObject('ParallelBruteForceBroadPhase',name='N2')
    rootNode.addObject('ParallelBVHNarrowPhase')
    rootNode.addObject('LocalMinDistance',contactDistance=1,alarmDistance=2,name='localmindistance',angleCone=0.5, coneFactor=0.5)
    rootNode.addObject('CollisionResponse',name='Response',response='FrictionContactConstraint')
    # rootNode.addObject('DefaultAnimationLoop')
    # rootNode.addObject('DefaultVisualManagerLoop')
    
    # setting VisualStyle, pluginList, and 3D frame coordinate
    rootNode.addObject('VisualStyle', displayFlags=display)
    rootNode.addObject('RequiredPlugin', pluginName=pluginList)
    rootNode.addObject('OglSceneFrame',style='Arrows', alignment='TopRight')
    rootNode.addObject('InteractiveCamera', name='Camera', position= [0,0,50], lookAt=[0,0,0])

    rootNode.gravity = [0.0, 0.0, 0.0] # mm/s^2
    radius = 1 #mm
    inner_radius = 0 
    StraightLength_stiff = 600 #mm
    StraightLength_soft = 400 #mm
    spireDiameter = 4000
    massDensity = 1550e-6 #g/mm^3
    youngModulus_stiff = 10000#N/mm^2 = 10000e6Pa (stiff)
    youngModulus_soft = 10000
    poissonRatio = 0.3
    nbsection_soft = 10
    nbsection_stiff = 40

    
    #---------------------------------------------------------------------------
    # setting catheter topology mesh and wireRestShape
    GuideCatheter = rootNode.addChild('GuideCatheter')
    # create straight Section, 60 sections, if want to import from external files using RodMeshSection
    GuideCatheter.addObject('RodStraightSection', name ='StraightSection_stiff',
                         youngModulus= youngModulus_stiff, poissonRatio= poissonRatio, radius = radius, nbEdgesCollis = nbsection_stiff, nbEdgesVisu = 160, length = StraightLength_stiff)
    GuideCatheter.addObject('RodSpireSection', name ='StraightSection_soft',
                         youngModulus= youngModulus_soft, poissonRatio= poissonRatio, radius = radius, nbEdgesCollis = nbsection_soft, nbEdgesVisu = 40, length = StraightLength_soft, spireDiameter=spireDiameter, spireHeight=0)
    

    GuideCatheter.addObject('WireRestShape', name='GC_RestShape',  
                                 printLog=True, template='Rigid3d', wireMaterials = '@StraightSection_stiff @StraightSection_soft')
    GuideCatheter.addObject('EdgeSetTopologyContainer', name='meshLinesBeam')
    GuideCatheter.addObject('EdgeSetTopologyModifier', name='Modifier')
    GuideCatheter.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
    GuideCatheter.addObject('MechanicalObject', name='dofTopo1', template='Rigid3d')
    


    #-----------------------------------------------------------------------
    # mechanical model of Catheter
    BeamModel = rootNode.addChild('BeamModel')
    
    BeamModel.addObject('EulerImplicitSolver', rayleighStiffness=0.2, printLog=False, rayleighMass=0.1)
    BeamModel.addObject('BTDLinearSolver', subpartSolve = False,verification = False, verbose=False)
    BeamModel.addObject('RegularGridTopology', name='MeshLines', drawEdges=False, 
                                    nx=180, ny=1, nz=1,
                                    xmax=1, xmin=0.0, ymin=0, ymax=0, zmax=1, zmin=1,
                                    p0=[0,0,0])
    BeamModel.addObject('MechanicalObject', showIndices=False, name='Instrument_DOFs', template='Rigid3d')
    # FEM method (BeamInterpolation)
    # plug the catheter RestShape into WireBeamInterpolation 
    BeamModel.addObject('WireBeamInterpolation', name='BeamInterpolation', WireRestShape='@../GuideCatheter/GC_RestShape', radius=radius, printLog=False)
    # compute internal forces
    # computeMass if false, only compute the stiff elastic model
    # massDensity: Density of the mass
    # shearStressComputation: if false, suppress the shear stress in the computation
    # reinforceLength: a separation computation for the error in elongation is performed
    BeamModel.addObject('AdaptiveBeamForceFieldAndMass', name='BeamForceField', massDensity=massDensity, interpolation='@BeamInterpolation', computeMass=True, reinforceLength= False, shearStressComputation= False)

    #Deployment Controller
    BeamModel.addObject('InterventionalRadiologyController', name='DeployController', template='Rigid3d', instruments='BeamInterpolation', 
                                    startingPos=[0,0,0,0,0,0,1], xtip=[1, 0, 0], printLog=False, 
                                    rotationInstrument=[0, 0, 0], step=3, speed=2, 
                                    listening=True, controlledInstrument=0)
    BeamModel.addObject('LinearSolverConstraintCorrection', wire_optimization=True)

    BeamModel.addObject('FixedConstraint', indices=0, name='FixedConstraint')
    # Add constraint box
    # box = [0,0,-50,120,6,70]
    # BeamModel.addObject('BoxROI',name='BoxROI',box = box, drawBoxes=True, doUpdate=False)
    BeamModel.addObject('RestShapeSpringsForceField', name="RestSPForceField", points='@DeployController.indexFirstNode', angularStiffness=1e8, stiffness=1e8)
    BeamModel.addObject('PartialFixedConstraint', fixedDirections = [0,0,1,0,0,0],indices=np.arange(180))
    #-----------------------------------------------------------------------
    # Collision model
    Collis = BeamModel.addChild('CollisionCatheter')
    Collis.activated = True
    Collis.addObject('MechanicalObject', name='colli_DOFs',template='Vec3d')
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
    Collis.addObject('MultiAdaptiveBeamMapping',controller='../DeployController',useCurvAbs=True, printLog=False,name='collisMap')
    Collis.addObject('PointCollisionModel',proximity=0.0)
    Collis.addObject('LineCollisionModel', proximity=0.0)
    # CollisionCatheter.addObject('TriangleCollisionModel')
    # CollisionCatheter.addObject('TetrahedronCollisionModel')
    
    #--------------------------------------------------------------------
    # Visual model: using WireRestShape mesh
    VisualCatheter = BeamModel.addChild('VisualCatheter')
    
    VisualCatheter.addObject('MechanicalObject', name= 'visu_DOFs',template='Vec3d')
    
    VisualCatheter.addObject('QuadSetTopologyContainer', name = "visu_container")
    VisualCatheter.addObject('QuadSetTopologyModifier')
    VisualCatheter.addObject('QuadSetGeometryAlgorithms')
    # Mapping WireRestShape mesh to topology container
    VisualCatheter.addObject('Edge2QuadTopologicalMapping', nbPointsOnEachCircle=10,
                             radius=radius, input='@../../GuideCatheter/meshLinesBeam', output='@visu_container')
    # Mapping mesh to Beam Mechanics
    VisualCatheter.addObject('AdaptiveBeamMapping', input="@../Instrument_DOFs", output="@visu_DOFs", interpolation='@../BeamInterpolation')
    
    # Visual beam by OglModel
    VisuOgl = VisualCatheter.addChild('VisuOgl')
    VisuOgl.addObject("OglModel", name="visual", color=[0.5,1,0.5], quads="@../visu_container.quads")
    VisuOgl.addObject('IdentityMapping', input="@../visu_DOFs",output='@visual')

    

    #---------------------------------------------------------------------
    # Noticed that, flipNormals has to be set to 1 here, in order to set Env Collision Model collide from inner wall.
    Env= rootNode.addChild('Env')
    Env.addObject('MeshSTLLoader', name = 'env_mesh', filename= 'Neurovascular_2D_2.stl', translation=[0, 0, -1.0], rotation= [0.0, 0.0, 0.0],triangulate=True, scale = 1)
    # Env.addObject('MeshSTLLoader', name = 'env_mesh', filename= 'flat_model_circles.stl', translation=[0, 0, -1.0], rotation= [0.0, 0.0, 0.0],triangulate=True, scale = 1)
    Env.addObject('MeshTopology', position = '@env_mesh.position', triangles= '@env_mesh.triangles', drawTriangles=False)
    Env.addObject('MechanicalObject', name = 'env_DOFs', scale=3)
    
    Env.addObject('PointCollisionModel', moving=False, simulated = False)
    Env.addObject('TriangleCollisionModel', moving=False, simulated = False)
    Env.addObject('LineCollisionModel', moving= False, simulated = False)
    Env.addObject('OglModel', name='visu_env', src='@env_mesh', color=[1,0,0,0.3], scale=3)

    return rootNode
    
