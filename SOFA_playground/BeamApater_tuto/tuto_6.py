# This file adds collision model into the actuator and add a carotids env
# Author: JunAng Wang
# Contact: wangjunang94@gmail.com
from stlib3.scene import MainHeader
from plugin_list import pluginList, display
def createScene(rootNode):

    # Header
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('DefaultVisualManagerLoop')
    rootNode.addObject('LCPConstraintSolver',mu=0.1,tolerance=1e-4,maxIt=1000,build_lcp=False)
    rootNode.addObject('CollisionPipeline',draw=0,depth=6,verbose='1')
    rootNode.addObject('BruteForceBroadPhase',name='N2')
    rootNode.addObject('BVHNarrowPhase')
    rootNode.addObject('LocalMinDistance',contactDistance=0.1,alarmDistance=2,name='localmindistance',angleCone=0.2)
    rootNode.addObject('CollisionResponse',name='Response',response='FrictionContactConstraint')
    # rootNode.addObject('DefaultAnimationLoop')
    # rootNode.addObject('DefaultVisualManagerLoop')
    
    # setting VisualStyle, pluginList, and 3D frame coordinate
    rootNode.addObject('VisualStyle', displayFlags=display)
    rootNode.addObject('RequiredPlugin', pluginName=pluginList)
    rootNode.addObject('OglSceneFrame',style='Arrows', alignment='TopRight')
    rootNode.gravity = [0.0, -9.81, 0.0] # mm/s^2
    radius = 1 #mm
    length = 1000 #mm
    StraightLength = 980
    SpireLength = 20
    massDensity = 0.00000155 #g/mm^3
    youngModulus = 20000#N/mm^2 = 170e6Pa (stiff)
    poissonRatio = 0.3
    nbsection = 60
    nbSpire = 10
    
    #---------------------------------------------------------------------------
    # setting catheter topology mesh and wireRestShape
    GuideCatheter = rootNode.addChild('GuideCatheter')
    # create straight Section, 60 sections, if want to import from external files using RodMeshSection
    GuideCatheter.addObject('RodStraightSection', name ='StraightSection',
                         youngModulus= youngModulus, poissonRatio= poissonRatio, radius = radius, massDensity=massDensity, nbEdgesCollis = nbsection-nbSpire, nbEdgesVisu = 200, length = StraightLength)
    GuideCatheter.addObject('RodSpireSection', name ='SpireSection',
                         youngModulus= youngModulus, poissonRatio= poissonRatio, radius = radius, massDensity=massDensity, nbEdgesCollis = nbSpire, nbEdgesVisu = 200, length = SpireLength, spireDiameter= 25, spireHeight = 0)

    GuideCatheter.addObject('WireRestShape', name='GC_RestShape',  
                                 printLog=True, template='Rigid3d', wireMaterials = '@StraightSection @SpireSection')
    GuideCatheter.addObject('EdgeSetTopologyContainer', name='meshLinesBeam')
    GuideCatheter.addObject('EdgeSetTopologyModifier', name='Modifier')
    GuideCatheter.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
    GuideCatheter.addObject('MechanicalObject', name='dofTopo2', template='Rigid3d')
    


    #-----------------------------------------------------------------------
    # mechanical model of Catheter
    BeamModel = rootNode.addChild('BeamModel')
    
    BeamModel.addObject('EulerImplicitSolver', rayleighStiffness=0.2, printLog=False, rayleighMass=0.1)
    BeamModel.addObject('BTDLinearSolver', verbose=False)
    BeamModel.addObject('RegularGridTopology', name='MeshLines', drawEdges=False, 
                                    nx=60, ny=1, nz=1,
                                    xmax=0.0, xmin=0.0, ymin=0, ymax=0, zmax=0, zmin=0,
                                    p0=[0,2,0])
    BeamModel.addObject('MechanicalObject', showIndices=False, name='Instrument_DOFs', template='Rigid3d')
    # FEM method (BeamInterpolation)
    # plug the catheter RestShape into WireBeamInterpolation 
    BeamModel.addObject('WireBeamInterpolation', name='BeamInterpolation', WireRestShape='@../GuideCatheter/GC_RestShape', radius=radius, printLog=False)
    # compute internal forces
    # computeMass if false, only compute the stiff elastic model
    # massDensity: Density of the mass
    # shearStressComputation: if false, suppress the shear stress in the computation
    # reinforceLength: a separation computation for the error in elongation is performed
    BeamModel.addObject('AdaptiveBeamForceFieldAndMass', name='BeamForceField', massDensity=massDensity, interpolation='@BeamInterpolation', computeMass=True, reinforceLength= False, shearStressComputation= True)

    #Deployment Controller
    BeamModel.addObject('InterventionalRadiologyController', name='DeployController', template='Rigid3d', instruments='BeamInterpolation', 
                                    startingPos=[0, 2, 0, 0, 0, 0, 1], xtip=[0, 0, 0], printLog=False, 
                                    rotationInstrument=[0, 0, 0], step=5, speed=5, 
                                    listening=True, controlledInstrument=0)
    BeamModel.addObject('LinearSolverConstraintCorrection', wire_optimization=True)

    BeamModel.addObject('FixedConstraint', indices=0, name='FixedConstraint')
    BeamModel.addObject('RestShapeSpringsForceField', name="RestSPForceField", points='@DeployController.indexFirstNode', angularStiffness=1e8, stiffness=1e8)

    
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
    VisuOgl.addObject("OglModel", name="visual", color=[0.7,0.7,0.7], quads="@../visu_container.quads")
    VisuOgl.addObject('IdentityMapping', input="@../visu_DOFs",output='@visual')

    #-----------------------------------------------------------------------
    # Collision model
    CollisionCatheter = BeamModel.addChild('CollisionCatheter')
    CollisionCatheter.addObject('MechanicalObject', name='colli_DOFs',template='Vec3d')
    # if use 1D line mesh, one can extend to 2D surf mesh
    # if one needs 3D mesh, one has to import stl 3D files or deploys CylinderGridTopology

    # CollisionCatheter.addObject('QuadSetTopologyContainer',name = 'colli_container')
    # CollisionCatheter.addObject('QuadSetTopologyModifier')
    # CollisionCatheter.addObject('QuadSetGeometryAlgorithms',showPointIndices=False, showEdgeIndices=False, drawEdges=False)
    # CollisionCatheter.addObject('Edge2QuadTopologicalMapping',nbPointsOnEachCircle=10,
    #                             radius=radius, input='@../../GuideCatheter/meshLinesBeam',
    #                             output='@colli_container')

    # CollisionCatheter.activated = True
    CollisionCatheter.addObject('EdgeSetTopologyContainer',name='collisEdgeSet')
    CollisionCatheter.addObject('EdgeSetTopologyModifier',name='colliseEdgeModifier')
    

    # CylinderGridTopology, nz is the longitudinal direction discretization
    # CollisionCatheter.addObject('CylinderGridTopology', name ='Cylinder_container', axis= [1,0,0], center = [0,0,0], length=length, radius=radius, nx=5, ny=5, nz=6)
    
    CollisionCatheter.addObject('PointCollisionModel', proximity=0.0)
    CollisionCatheter.addObject('LineCollisionModel', proximity=0.0)
    # CollisionCatheter.addObject('TriangleCollisionModel')
    # CollisionCatheter.addObject('TetrahedronCollisionModel')
    CollisionCatheter.addObject('MultiAdaptiveBeamMapping',controller='../DeployController',useCurvAbs=True, printLog=False,name='collisMap')
    # CollisionCatheter.addObject('AdaptiveBeamMapping', isMechanical=True, input='@../Instrument_DOFs', output='@colli_DOFs')

    #---------------------------------------------------------------------
    Env = rootNode.addChild('Env')
    Env.addObject('MeshSTLLoader', name = 'env_mesh', filename= 'carotids.stl', translation=[0, 0, 0.0], rotation= [0.0, 0.0, 90.0],triangulate=True,)
    Env.addObject('MeshTopology', position = '@env_mesh.position', triangles= '@env_mesh.triangles', drawTriangles=False)
    Env.addObject('MechanicalObject', name = 'env_DOFs')
    
    Env.addObject('PointCollisionModel', moving=False, simulated = False)
    Env.addObject('TriangleCollisionModel', moving=False, simulated = False)
    Env.addObject('LineCollisionModel', moving= False, simulated = False)

    return rootNode
    
