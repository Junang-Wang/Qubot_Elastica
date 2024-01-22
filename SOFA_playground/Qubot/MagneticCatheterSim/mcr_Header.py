from MagneticCatheterSim.plugin_list import pluginList, display

def Header(
        rootNode,
        dt = 0.01,
        gravity = [0.0,0.0,0.0],
        mu = 0.1,
        contactDistance = 1,
        alarmDistance = 2,
        angleCone = 0.5,
        coneFactor = 0.5,
):
    '''
    Header function sets up the AnimationLoop, Constraint Solver, Collision Detection, Collision Response, gravity and time step
    dt             : time step
    gravity        : gravity mm/s^2
    mu             : friction coefficient
    contactDistance: minimum distance acceptable below which the contact is created and the objects can't be closer at the contact location
    alarmDistance  : distance until which a contact between two objects is detected
    angleCone      : Filtering cone extension angle
    coneFactor     : Factor for filtering cone angle computation
    '''
    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('DefaultVisualManagerLoop')
    # Constraint Solver
    rootNode.addObject('LCPConstraintSolver',mu=mu,tolerance=1e-4,maxIt=1000,build_lcp=False)
    rootNode.addObject('CollisionPipeline',draw=0,depth=6,verbose='1')
    rootNode.addObject('ParallelBruteForceBroadPhase',name='N2')
    rootNode.addObject('ParallelBVHNarrowPhase')
    rootNode.addObject('LocalMinDistance',contactDistance=contactDistance,alarmDistance=alarmDistance,name='localmindistance',angleCone=angleCone, coneFactor=coneFactor)
    rootNode.addObject('CollisionResponse',name='Response',response='FrictionContactConstraint')
    # rootNode.addObject('DefaultAnimationLoop')
    # rootNode.addObject('DefaultVisualManagerLoop')
    
    # setting VisualStyle, pluginList, and 3D frame coordinate
    rootNode.addObject('VisualStyle', displayFlags=display)
    rootNode.addObject('BackgroundSetting', color=[0,0,0,1])
    rootNode.addObject('RequiredPlugin', pluginName=pluginList)
    rootNode.addObject('OglSceneFrame',style='Arrows', alignment='TopRight')
    rootNode.addObject('InteractiveCamera', name='Camera', position= [0,0,50], lookAt=[0,0,0])
    rootNode.gravity = gravity # mm/s^2
    rootNode.dt = dt
        