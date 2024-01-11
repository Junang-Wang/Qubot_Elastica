# This file indicates the visualization by importing a mesh stl file.
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
    GuideCatheter.addObject('RodStraightSection', name= "StraightSection", youngModulus = 1e5, poissonRatio = 0.3, radius = 0.1, massDensity = 1, nbEdgesCollis=5, nbEdgesVisu = 5, length=3)
    GuideCatheter.addObject('WireRestShape', template = 'Rigid3d', name = 'RestShape', wireMaterials = "@StraightSection")
    GuideCatheter.addObject('EdgeSetTopologyContainer', name='Catheter_mesh', src="@RestShape")
    GuideCatheter.addObject('EdgeSetTopologyModifier')
    GuideCatheter.addObject('MechanicalObject', template='Rigid3d',
                        name = 'DOFs')
    GuideCatheter.addObject('EdgeSetGeometryAlgorithms',template="Rigid3d")

    # mechanical model of Catheter
    BeamModel = GuideCatheter.addChild('BeamModel')
    BeamModel.addObject('EulerImplicitSolver', rayleighStiffness=0.2, 
                        rayleighMass=0.1, printLog=False)
    BeamModel.addObject('BTDLinearSolver', verbose =0)
    
    BeamModel.addObject("MeshTopology", src = "@../Catheter_mesh")
    BeamModel.addObject('MechanicalObject',name= "Instrument_DOFs", template='Rigid3d', src="@../Catheter_mesh", showObject=True, showObjectScale= 0.1)
    # FEM method (BeamInterpolation)
    # plug the catheter RestShape into BeamInterpolation 
    BeamModel.addObject('BeamInterpolation', name= 'BeamInterpolation', radius = 0.1) 
    # compute internal forces
    # computeMass if false, only compute the stiff elastic model
    # massDensity: Density of the mass
    # shearStressComputation: if false, suppress the shear stress in the computation
    # reinforceLength: a separation computation for the error in elongation is performed
    BeamModel.addObject('AdaptiveBeamForceFieldAndMass', name='BeamForceField', interpolation = "@BeamInterpolation",
                        computeMass=True, massDensity = 1, reinforceLength= False, shearStressComputation = True)
    BeamModel.addObject('FixedConstraint', name= 'FixedConstraint',indices = 0)
    
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
    
