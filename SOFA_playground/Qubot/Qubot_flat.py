
from stlib3.scene import MainHeader, ContactHeader

# env_stl = '../mesh/flat_models/flat_model_circles.stl'
env_stl = '../mesh/flat_models/Neurovascular_2D.stl'
# env_stl = '../mesh/3D_models/Neurovascular_3D.stl'
pluginList = ['Sofa.Component.Collision.Geometry',
              'Sofa.Component.IO.Mesh',
              'Sofa.Component.LinearSolver.Iterative',
              'Sofa.Component.Mapping.NonLinear',
              'Sofa.Component.ODESolver.Backward',
              'Sofa.Component.StateContainer',
              'Sofa.Component.Topology.Container.Constant',
              'Sofa.Component.Visual',
              'Sofa.GL.Component.Rendering3D']
def createScene(root_node):

    MainHeader(root_node, gravity = [0.0, 0.0, 0.0], plugins=pluginList)

    root_node.addObject('DefaultAnimationLoop')
    root_node.addObject('Camera', position= [0.0,20.0,0.0], lookAt=[0.0,0.0,0.0])
    root_node.VisualStyle.displayFlags ="showVisual showBehavior"
    # mechanical model
    env = root_node.addChild('env')
    env.addObject('MechanicalObject', name='env', 
                              template='Rigid3d', translation=[-155.0, 80.0, 0.0], rotation= [0.0, 0.0, 0.0])
    
    env.addObject('MeshSTLLoader', name='env_Loader', filename=env_stl)

    # Time integration and solver
    env.addObject('EulerImplicitSolver', name='odesolver')
    env.addObject('CGLinearSolver', name='Solver', iterations=25, tolerance=1e-5, threshold=1e-5)

    # visual model
    env_visual = env.addChild('env_visual')
    # env_visual.addObject('MeshSTLLoader', name='Loader', filename=env_stl)
    env_visual.addObject(
            'OglModel',
            name="VisualOgl_model",
            src='@../env_Loader', scale=1)
    env_visual.addObject('RigidMapping')

    # collision model

    env_collision = env.addChild('env_collision')
    env_collision.addObject('MeshTopology', src='@../env_Loader')

    env_collision.addObject('MechanicalObject')
    # deformable
#     env_collision.addObject('TetrahedronSetTopologyContainer',name='meshContainer',src='@../env_Loader')
#     env_collision.addObject('TetrahedronSetGeometryAlgorithms', template= 'Vec3d',name = 'GeomAlgo')


    env_collision.addObject('TriangleCollisionModel')
#     env_collision.addObject('LineCollisionModel')
#     env_collision.addObject('PointCollisionModel')

    env_collision.addObject('RigidMapping')

    return root_node