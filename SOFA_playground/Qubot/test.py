# Required import for python
import Sofa

def main():
    import SofaRuntime
    import Sofa.Gui
    # Make sure to load all SOFA libraries
    SofaRuntime.importPlugin("SofaBaseMechanics")
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("CImgPlugin")

    #Create the root node
    root = Sofa.Core.Node("root")
    # Call the below 'createScene' function to create the scene graph
    createScene(root)
    Sofa.Simulation.init(root)

    # Find out the supported GUIs
    print ("Supported GUIs are: " + Sofa.Gui.GUIManager.ListSupportedGUI(","))
    # Launch the GUI (qt or qglviewer)
    Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1080, 1080)
    # Initialization of the scene will be done here
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()
    print("GUI was closed")


# Function called when the scene graph is being created
def createScene(root):

    root.gravity=[0, 0, 0]
    root.name="root"
    root.dt=0.01
    
    root.addObject('RequiredPlugin', name="loadSOFAModules", pluginName="Sofa.Component.LinearSolver.Iterative Sofa.Component.Mass Sofa.Component.MechanicalLoad Sofa.Component.StateContainer Sofa.Component.ODESolver.Backward")
    root.addObject('DefaultAnimationLoop', computeBoundingBox=False)
    root.addObject('BackgroundSetting', color="0 0 1 1")    

    return root


# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
