import sys,os
parent_dir = os.path.abspath('..')
sys.path.append(parent_dir)
print(sys.path)
from M_rod_packages import *
from Plot_Method import *
from tqdm import tqdm
def Data_Generator(end_time, amplitude_period, direction_period,step_skip=100):
    global magnetic_field
    magnetic_amplitude = 0
    magnetic_field_direction = np.array([0.0,0.0,1.0])
    normal_direction = np.array([1.0,0.0]) # magnetic field normal direction in yz plane
    scale_E = 1e-3 # scale down Young's module and magnetic torque at the same time to prevent numerical problems
    magnetic_field = magnetic_field_direction*magnetic_amplitude * scale_E
    magnetic_amplitude_max = 60e3
#------------------icon and screen setting ----------
    current_dir = os.path.dirname(__file__)
    
#----------------PyElastica Simulator-------------
    class UnitMagneticRodSimulator(BaseSystemCollection, Constraints, Forcing, Damping, CallBacks):
        pass
    Uniform_M_Sim = UnitMagneticRodSimulator()
    dt = 1.4e-4 # time step
    time = 0
    do_step, stages_and_updates, timestepper, M_rod, M_list = Sim_init(Uniform_M_Sim, magnetic_field, dt=dt, scale_E=scale_E, step_skip=step_skip)


    tspan = np.arange(0,end_time,dt)
    for time in tqdm(tspan):
        magnetic_amplitude = magnetic_amplitude_max*scale_E*np.sin(2*np.pi/amplitude_period*time)
        magnetic_field[1] = magnetic_amplitude* np.sin(2*np.pi/direction_period*time)
        magnetic_field[2] = magnetic_amplitude* np.cos(2*np.pi/direction_period*time)
        do_step(timestepper, stages_and_updates, Uniform_M_Sim, time, dt)
    
    return M_list


        
    
