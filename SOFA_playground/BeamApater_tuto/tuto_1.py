# This files indicate that import mesh file to collision model
# Author: JunAng Wang
# Contact: wangjunang94@gmail.com
from stlib3.scene import MainHeader
from plugin_list import pluginList, display
def createScene(rootNode):

    # Header
    rootNode.addObject('DefaultAnimationLoop')
    rootNode.addObject('DefaultVisualManagerLoop')
    rootNode.addObject('VisualStyle', displayFlags=display)
    rootNode.addObject('RequiredPlugin', pluginName=pluginList)
    rootNode.addObject('OglSceneFrame',style='Arrows', alignment='TopRight')
    rootNode.gravity = [0.0, -9.81, 0.0]
    
    BeamModel = rootNode.addChild('BeamModel')
    BeamModel.addObject('EulerImplicitSolver', rayleighStiffness=0, 
                        rayleighMass=0, printLog=False)
    BeamModel.addObject('BTDLinearSolver', verbose =0)
    positions = [[0,0,2,0,0,0,1],[1,0,2,0,0,0,1],[2,0,2,0,0,0,1],[3,0,2,0,0,0,1]]
    # wireRestShape
    BeamModel.addObject('MechanicalObject', template='Rigid3d',
                        name = 'DOFs', position = positions)
    # lines is alias of edges
    BeamModel.addObject('MeshTopology', name="lines", edges= [0,1,1,2,2,3])
    BeamModel.addObject('FixedConstraint', name= 'FixedConstraint',indices = 0)
    # FEM method (BeamInterpolation)
    # define YoungModulus and PoissonRation if they are not defined
    BeamModel.addObject('BeamInterpolation', name= 'BeamInterpolation', radius = 0.1, defaultYoungModulus=1e5, defaultPoissonRatio = 0.3) 
    # compute internal forces
    # computeMass if false, only compute the stiff elastic model
    # massDensity: Density of the mass
    # shearStressComputation: if false, suppress the shear stress in the computation
    # reinforceLength: a separation computation for the error in elongation is performed
    BeamModel.addObject('AdaptiveBeamForceFieldAndMass', name='BeamForceField', 
                        computeMass=True, massDensity = 10, reinforceLength= False, shearStressComputation = True)
    
    Collision = BeamModel.addChild('Collision')
    Collision.addObject('MeshSTLLoader', name= "cylinder_Loader", filename="cylinder.stl")
    Collision.addObject('TriangleSetTopologyContainer', name = "cylinder_topo", src = "@cylinder_Loader")
    Collision.addObject('TriangleSetTopologyModifier')
    Collision.addObject('MechanicalObject', name= 'collision',template='Vec3d')
    Collision.addObject('TriangleSetGeometryAlgorithms')
    Collision.addObject('TriangleCollisionModel', color =[0.5, 1, 0.5, 1])
    Collision.addObject('AdaptiveBeamMapping', input="@../DOFs", output="@collision")

    return rootNode
    
