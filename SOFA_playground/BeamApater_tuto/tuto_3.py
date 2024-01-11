# This file deploys the actuator 
# Author: JunAng Wang
# Contact: wangjunang94@gmail.com
from stlib3.scene import MainHeader
from plugin_list import pluginList, display
def createScene(rootNode):

    # Header
    rootNode.addObject('DefaultAnimationLoop')
    rootNode.addObject('DefaultVisualManagerLoop')
    # setting VisualStyle, pluginList, and 3D frame coordinate
    rootNode.addObject('VisualStyle', displayFlags=display)
    rootNode.addObject('RequiredPlugin', pluginName=pluginList)
    rootNode.addObject('OglSceneFrame',style='Arrows', alignment='TopRight')
    rootNode.gravity = [0.0, -9.81, 0.0]
    

    # setting catheter topology mesh and wireRestShape
    GuideCatheter = rootNode.addChild('GuideCatheter')
    # create straight Section, 5 sections
    GuideCatheter.addObject('RodStraightSection', name ='StraightSection',
                         youngModulus= 1e5, poissonRatio=0.3, radius = 1, massDensity=1, nbEdgesCollis = 5, nbEdgesVisu = 5, length = 3)

    GuideCatheter.addObject('WireRestShape', name='GC_RestShape',  
                                 printLog=True, template='Rigid3d', wireMaterials = '@StraightSection')
    GuideCatheter.addObject('EdgeSetTopologyContainer', name='meshLinesBeam')
    GuideCatheter.addObject('EdgeSetTopologyModifier', name='Modifier')
    GuideCatheter.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
    GuideCatheter.addObject('MechanicalObject', name='dofTopo2', template='Rigid3d')


    # mechanical model of Catheter
    BeamModel = rootNode.addChild('BeamModel')
    BeamModel.addObject('EulerImplicitSolver', rayleighStiffness=0.2, printLog=False, rayleighMass=0.1)
    BeamModel.addObject('BTDLinearSolver', verbose=False)
    BeamModel.addObject('RegularGridTopology', name='MeshLines', drawEdges=False, 
                                    nx=60, ny=1, nz=1,
                                    xmax=0.0, xmin=0.0, ymin=0, ymax=0, zmax=0, zmin=0,
                                    p0=[0,0,0])
    # Don't use meshLinesBeam as mesh topology for actuator since actuator mesh is dynamical.
    # BeamModel.addObject('MeshTopology',src='@../GuideCatheter/meshLinesBeam') 
    BeamModel.addObject('MechanicalObject', showIndices=False, name='Instrument_DOFs', template='Rigid3d')
    # FEM method (BeamInterpolation)
    # plug the catheter RestShape into WireBeamInterpolation 
    BeamModel.addObject('WireBeamInterpolation', name='BeamInterpolation', WireRestShape='@../GuideCatheter/GC_RestShape', 
                                    radius=0.1, printLog=False)
    # compute internal forces
    # computeMass if false, only compute the stiff elastic model
    # massDensity: Density of the mass
    # shearStressComputation: if false, suppress the shear stress in the computation
    # reinforceLength: a separation computation for the error in elongation is performed
    BeamModel.addObject('AdaptiveBeamForceFieldAndMass', name='BeamForceField', massDensity=1, interpolation='@BeamInterpolation', computeMass=True, reinforceLength= False, shearStressComputation= True)

    #Deployment Controller
    BeamModel.addObject('InterventionalRadiologyController', name='DeployController', template='Rigid3d', instruments='BeamInterpolation', 
                                    startingPos=[0, 0, 0, 0, 0, 0, 1], xtip=[0, 0, 0], printLog=True, 
                                    rotationInstrument=[0, 0, 0], step=0.5, speed=0.5, 
                                    listening=True, controlledInstrument=0)
    BeamModel.addObject('FixedConstraint', indices=0, name='FixedConstraint')
    BeamModel.addObject('RestShapeSpringsForceField', name="RestSPForceField", points='@DeployController.indexFirstNode', angularStiffness=1e8, stiffness=1e8)

    # Visual model: Load the Catheter mesh file
    VisualCatheter = BeamModel.addChild('VisualCatheter')
    VisualCatheter.addObject('MeshSTLLoader', name= "cylinder_Loader", filename="cylinder.stl")
    VisualCatheter.addObject('TriangleSetTopologyContainer', name = "cylinder_container", src = "@cylinder_Loader")
    VisualCatheter.addObject('TriangleSetTopologyModifier')
    VisualCatheter.addObject('MechanicalObject', name= 'visu_DOFs',template='Vec3d')
    VisualCatheter.addObject('TriangleSetGeometryAlgorithms')
    # Mapping mesh to Beam Mechanics
    VisualCatheter.addObject('AdaptiveBeamMapping', input="@../Instrument_DOFs", output="@visu_DOFs", interpolation='@../BeamInterpolation')
    
    # Visual beam by OglModel
    VisuOgl = VisualCatheter.addChild('VisuOgl')
    VisuOgl.addObject("OglModel", name="visual", color=[0.7,0.7,0.7], triangles="@../cylinder_container.triangles")
    VisuOgl.addObject('IdentityMapping', input="@../visu_DOFs",output='@visual')

    return rootNode
    
