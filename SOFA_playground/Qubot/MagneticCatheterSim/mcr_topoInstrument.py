import Sofa 
import numpy as np 

class Topo_Instrument():
    '''
    topology of instrument
    shapes    : shape of instrument
    radius    : radius of instrument (mm)
    inner_radius : inner radius of instrument (mm)
    StraightLengths: length 
    massDensity    : density of mass
    youngModulus   : young's modulus
    poissonRatio   : poisson Ratio
    nbsections     : number of sections
    nbsections_visu: number of visual sections
    '''
    def __init__(
        self,
        rootNode,
        name = 'GuideCatheter',
        shapes = ['StraightSection','SpireSection'],
        radius = 1, #mm/ 1000 = m, radius has to be the same for an individual instrument
        inner_radius = 0,
        StraightLengths = [600, 40], #mm 
        spireDiameter = [0,4000],
        spireHeight = [0,0],
        massDensity = 1550 * 1e-6, #g/mm^3, mass density has to the same for an individual instrument
        youngModulus = [10000e3,10000e3],#10000e3Pa (stiff)
        poissonRatio = [1/3,1/3],
        nbsections = [40,10],
        nbsections_visu = [160,40],
    ):
        
        self.instrument = rootNode.addChild(name)
        self.radius = radius
        self.inner_radius = inner_radius
        self.StraightLengths = StraightLengths
        self.massDensity = massDensity
        self.youngModulus = youngModulus
        self.poissonRatio = poissonRatio
        self.nbsections = nbsections
        self.name = name
        # setting instruments topology mesh and wireRestShape

        # create straight Section, 50 sections, if want to import from external files using RodMeshSection
        wireMaterials = []
        for i in range(len(shapes)):
            self.sectionName = name+shapes[i]+f'_{i}'
            wireMaterials.append('@'+self.sectionName)
            if shapes[i] == 'StraightSection':
                self.instrument.addObject(
                    'RodStraightSection',
                    name = self.sectionName,
                    youngModulus= youngModulus[i], 
                    poissonRatio= poissonRatio[i], 
                    radius = radius,
                    innerRadius=inner_radius, 
                    nbEdgesCollis = nbsections[i], 
                    nbEdgesVisu = nbsections_visu[i], 
                    length = StraightLengths[i])
            elif shapes[i] == 'SpireSection':
                self.instrument.addObject(
                    'RodSpireSection', 
                    name =name+f'StraightSection_{i}',
                    youngModulus= youngModulus[i], 
                    poissonRatio= poissonRatio[i],
                    radius = radius, 
                    innerRadius = inner_radius,
                    nbEdgesCollis = nbsections[i], 
                    nbEdgesVisu = nbsections_visu[i], 
                    length = StraightLengths[i], spireDiameter=spireDiameter[i], 
                    spireHeight=spireHeight[i])
        self.WireRestShapeName = name + '_RestShape'
        self.instrument.addObject(
            'WireRestShape', 
            name= self.WireRestShapeName,  
            printLog=False, 
            template='Rigid3d', 
            wireMaterials = ' '.join(wireMaterials))
        self.instrument.addObject('EdgeSetTopologyContainer', name='meshLinesBeam')
        self.instrument.addObject('EdgeSetTopologyModifier', name='Modifier')
        self.instrument.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
        self.instrument.addObject('MechanicalObject', name='dofTopo1', template='Rigid3d')
        

        
