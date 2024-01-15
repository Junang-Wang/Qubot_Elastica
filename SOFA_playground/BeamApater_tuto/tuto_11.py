# This file adds collision model into the actuator and add a env. Meanwhile constrains catheter to 2D.
# now Catheter contains two sections, one is stiff and the other is softer. The parameters of Catheter 
# use SOFA example parameters. In the unit of mm, kg.
# Here is the example edited by '3instruments_collision.scn'
# Author: JunAng Wang
# Contact: wangjunang94@gmail.com
from stlib3.scene import MainHeader
from plugin_list import pluginList, display
import numpy as np
def createScene(rootNode):

    # Header
    rootNode.addObject('DefaultVisualManagerLoop')
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('LCPConstraintSolver',mu=0.1,tolerance=1e-4,maxIt=1000,build_lcp=False)
    rootNode.addObject('CollisionPipeline',draw=0,depth=6,verbose='1')
    rootNode.addObject('BruteForceBroadPhase',name='N2')
    rootNode.addObject('BVHNarrowPhase')
    rootNode.addObject('LocalMinDistance',contactDistance=1,alarmDistance=2,name='localmindistance',angleCone=0.5, coneFactor=0.5)
    rootNode.addObject('CollisionResponse',name='Response',response='FrictionContactConstraint')
    
    # setting VisualStyle, pluginList, and 3D frame coordinate
    rootNode.addObject('VisualStyle', displayFlags=display)
    rootNode.addObject('RequiredPlugin', pluginName=pluginList)
    rootNode.addObject('OglSceneFrame',style='Arrows', alignment='TopRight')
    rootNode.addObject('InteractiveCamera', name='Camera', position= [-50,0,0], lookAt=[0,0,0])

    rootNode.gravity = [0.0, 0.0, 0.0] # mm/s^2
        
    #---------------------------------------------------------------------------
    # setting catheter topology mesh and wireRestShape
    topoLines = rootNode.addChild('topoLines_cath')
    # create straight Section, 60 sections, if want to import from external files using RodMeshSection
    topoLines.addObject('RodStraightSection', name ='StraightSection',
                         youngModulus= 10000, poissonRatio = 0.3, nbEdgesCollis = 40, nbEdgesVisu = 220, length = 600)
    topoLines.addObject('RodSpireSection', name ='SpireSection',
                         youngModulus= 10000, poissonRatio = 0.3,nbEdgesCollis = 10, nbEdgesVisu = 80, length = 400, spireDiameter=4000, spireHeight=0)
    

    topoLines.addObject('WireRestShape', name='catheterRestShape',  
                                template='Rigid3d', wireMaterials = '@StraightSection @SpireSection')
    topoLines.addObject('EdgeSetTopologyContainer', name='meshLinesBeam')
    topoLines.addObject('EdgeSetTopologyModifier', name='Modifier')
    topoLines.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
    topoLines.addObject('MechanicalObject', name='dofTopo1', template='Rigid3d')
    


    #-----------------------------------------------------------------------
    # mechanical model of Catheter
    InstrumentCombined = rootNode.addChild('InstrumentCombined')
    
    InstrumentCombined.addObject('EulerImplicitSolver', rayleighStiffness=0.2, printLog=False, rayleighMass=0.1)
    InstrumentCombined.addObject('BTDLinearSolver',subpartSolve=False, verification=False, verbose=False)
    InstrumentCombined.addObject('RegularGridTopology', name='MeshLines', 
                                    nx=180, ny=1, nz=1,
                                    xmax=1.0, xmin=0.0, ymin=0, ymax=0, zmax=1, zmin=1,
                                    p0=[0,0,0])
    InstrumentCombined.addObject('MechanicalObject', name='DOFs', template='Rigid3d', ry=-90)
    # FEM method (BeamInterpolation)
    # plug the catheter RestShape into WireBeamInterpolation 
    InstrumentCombined.addObject('WireBeamInterpolation', name='InterpolCatheter', WireRestShape='@../topoLines_cath/catheterRestShape', radius=1, printLog=False)
    # compute internal forces
    # computeMass if false, only compute the stiff elastic model
    # massDensity: Density of the mass
    # shearStressComputation: if false, suppress the shear stress in the computation
    # reinforceLength: a separation computation for the error in elongation is performed
    InstrumentCombined.addObject('AdaptiveBeamForceFieldAndMass', name='CatheterForceField', massDensity= 0.00000155, interpolation='@InterpolCatheter')

    #Deployment Controller
    InstrumentCombined.addObject('InterventionalRadiologyController', name='IRController', template='Rigid3d', instruments='InterpolCatheter', 
                                    startingPos=[0,0,0,0,-0.7071068,0,0.7071068], xtip=[1, 0, 0], printLog=False, 
                                    rotationInstrument=[0, 0, 0], step=3, speed=2, 
                                    listening=True, controlledInstrument=0)
    InstrumentCombined.addObject('LinearSolverConstraintCorrection', wire_optimization=True)

    InstrumentCombined.addObject('FixedConstraint', indices=0, name='FixedConstraint')
    # Add constraint box
    # box = [0,0,-50,120,6,70]
    # BeamModel.addObject('BoxROI',name='BoxROI',box = box, drawBoxes=True, doUpdate=False)
    InstrumentCombined.addObject('RestShapeSpringsForceField', name="RestSPForceField", points='@IRController.indexFirstNode', angularStiffness=1e8, stiffness=1e8)
    # BeamModel.addObject('PartialFixedConstraint', indices = np.arange(nbsection_stiff + nbsection_soft), fixedDirections = [0,0,1,0,0,0])
    
    #-----------------------------------------------------------------------
    # Collision model
    Collis = InstrumentCombined.addChild('Collis')
    Collis.activated = True
    # if use 1D line mesh, one can extend to 2D surf mesh
    # if one needs 3D mesh, one has to import stl 3D files or deploys CylinderGridTopology

    Collis.addObject('EdgeSetTopologyContainer',name='collisEdgeSet')
    Collis.addObject('EdgeSetTopologyModifier',name='colliseEdgeModifier')
    Collis.addObject('MechanicalObject', name='collisionDOFs')
    
    Collis.addObject('MultiAdaptiveBeamMapping',controller='../IRController',useCurvAbs=True, printLog=False,name='collisMap')
    Collis.addObject('PointCollisionModel', proximity = 0.0, group ='1')
    Collis.addObject('LineCollisionModel', proximity=0.0, group = '1')

    #--------------------------------------------------------------------
    # Visual model: using WireRestShape mesh
    VisuCatheter = InstrumentCombined.addChild('VisuCatheter')
    VisuCatheter.activated = True
    
    VisuCatheter.addObject('MechanicalObject', name= 'Quads')
    VisuCatheter.addObject('QuadSetTopologyContainer', name = "ContainerCath")
    VisuCatheter.addObject('QuadSetTopologyModifier')
    VisuCatheter.addObject('QuadSetGeometryAlgorithms', template='Vec3d')
    # Mapping WireRestShape mesh to topology container
    VisuCatheter.addObject('Edge2QuadTopologicalMapping', nbPointsOnEachCircle=10,
                             radius=2, input='@../../topoLines_cath/meshLinesBeam', output='@ContainerCath', flipNormals= '1')
    # Mapping mesh to Beam Mechanics
    VisuCatheter.addObject('AdaptiveBeamMapping', name='VisuMapCath', useCurvAbs=True, input="@../DOFs", output="@Quads", interpolation='@../InterpolCatheter', isMechanical=False)

    
    # Visual beam by OglModel
    VisuOgl = VisuCatheter.addChild('VisuOgl')
    VisuOgl.addObject("OglModel", name="Visual", color=[0.7,0.7,0.7], quads="@../ContainerCath.quads")
    VisuOgl.addObject('IdentityMapping', input="@../Quads",output='@Visual')

   
    #---------------------------------------------------------------------
    CollisionModel = rootNode.addChild('CollisionModel')
    CollisionModel.addObject('MeshOBJLoader', name = 'meshLoader', filename= 'phantom.obj',triangulate=True, flipNormals='1')
    # Env.addObject('MeshSTLLoader', name = 'env_mesh', filename= 'flat_model_circles.stl', translation=[0, 0, -3.0], rotation= [0.0, 0.0, 0.0],triangulate=True, scale = 1)
    CollisionModel.addObject('MeshTopology', position = '@meshLoader.position', triangles= '@meshLoader.triangles', drawTriangles=False)
    CollisionModel.addObject('MechanicalObject', name = 'DOFs1', position=[0,0,400], scale=3, ry=90)
    
    CollisionModel.addObject('PointCollisionModel', moving=False, simulated = False)
    CollisionModel.addObject('TriangleCollisionModel', moving=False, simulated = False)
    CollisionModel.addObject('LineCollisionModel', moving= False, simulated = False)
    CollisionModel.addObject('OglModel', name='Visual', src='@meshLoader', color=[1,0,0,0.3], scale=3, ry=90)

    return rootNode
    
