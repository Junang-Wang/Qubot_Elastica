def environment(
        rootNode,
        name,
        filename,
        translation,
        rotation,
        scale,
        color = [1,0,0,0.3]
):
    '''
    This function initializes the Env collision model
    name       : name of Env collision model
    filename   : location of Env mesh
    translation: translation of the mesh
    rotation   : rotation of the mesh
    color      : color of mesh [red, green, blue, transparency]
    '''
    # Noticed that, flipNormals has to be set to 1 here, in order to set Env Collision Model collide from inner wall.
    Env= rootNode.addChild(name)
    Env.addObject(
        'MeshSTLLoader', 
        name = 'env_mesh', 
        filename= filename, 
        translation= translation, 
        rotation= rotation,
        triangulate=True, 
        scale = scale)
    Env.addObject(
        'MeshTopology', 
        position = '@env_mesh.position', 
        triangles= '@env_mesh.triangles', drawTriangles=False)
    Env.addObject(
        'MechanicalObject', 
        name = 'env_DOFs', 
        scale=1)
    
    Env.addObject('PointCollisionModel', moving=False, simulated = False)
    Env.addObject('TriangleCollisionModel', moving=False, simulated = False)
    Env.addObject('LineCollisionModel', moving= False, simulated = False)
    Env.addObject('OglModel', name='visu_env', src='@env_mesh', color= color, scale=1)