import numpy as np
from elastica import *
from magneto_pyelastica import *
def Sim_init(Uniform_M_Sim, magnetic_field, density = 2.273, base_length = 6, base_radius = 0.3,scale_E=1e-3, E= 1.4e9, dt = 1.4e-4, nu =5):
    #--------mmGS unit----------
    '''
    density = 2.273  #mg/mm^3 
    base_length = 6 #mm 
    base_radius = 0.3 #mm 
    scale_E = 1e-3 #scale dowing Young's modulus
    E = 1.4e9 * scale_E #Young's modulus
    shear_modulus = E/3  # shear modulus


    dt = 1.4e-4 # time step
    nu = 5
    '''
    E = E* scale_E
    shear_modulus = E/3
    endtime = 5000

    #--------rod definition-------
    n_elem = 40
    start = np.array([0.0,0.0,0.0])
    direction = np.array([0.0,1.0,0.0])
    normal = np.array([1.0,0.0,0.0])
    M_rod = CosseratRod.straight_rod(n_elem, start, direction, normal, base_length, base_radius, density, youngs_modulus=E, shear_modulus=shear_modulus)

    Uniform_M_Sim.append(M_rod)
    #--------magnetic properties-----
    # sclae_E_s = 1e2 # separate contribution of density and magnetic field
    magnetization_density = 1.28e5 * 1e-3 #A/mm
    

    magnetization_direction = np.ones((n_elem)) * direction.reshape(3, 1)

    #------set the constant magnetic field object-----
    # rescale_magnetic_amplitude = magnetic_amplitude*scale_E # mg/(s^2*A)
    # magnetic_field = rescale_magnetic_amplitude* magnetic_field_direction

    magnetic_field_object = ConstantMagneticField(
        magnetic_field, ramp_interval = 0.1, start_time = 0, end_time = endtime
    )

    #--------constrain----------
    Uniform_M_Sim.constrain(M_rod).using(
        OneEndFixedBC, constrained_position_idx=(0,), constrained_director_idx=(0,)
    )

    #--------damping------------
    Uniform_M_Sim.dampen(M_rod).using(
        AnalyticalLinearDamper, damping_constant = nu, time_step = dt
    )
    #--------force--------------
    Uniform_M_Sim.add_forcing_to(M_rod).using(
        MagneticForces,
        external_magnetic_field = magnetic_field_object,
        magnetization_density = magnetization_density,
        magnetization_direction = magnetization_direction,
        rod_volume = M_rod.volume,
        rod_director_collection = M_rod.director_collection.copy(),
    )
    #------callback function------
    class MagneticRodCallBack(CallBackBaseClass):
        def __init__(self, step_skip:int, callback_params:dict):
            super().__init__()
            self.step_skip = step_skip
            self.callback_params = callback_params
        
        def make_callback(self, system, time, current_step: int):
            if current_step % self.step_skip == 0:
                self.callback_params["time"].append(time)
                self.callback_params["position"].append(system.position_collection.copy())
                self.callback_params["velocity"].append(system.velocity_collection.copy())
                return
    MR_list = defaultdict(list)
    Uniform_M_Sim.collect_diagnostics(M_rod).using(
        MagneticRodCallBack, step_skip = 100, callback_params = MR_list
    )

    Uniform_M_Sim.finalize()
    #--------time integration-----
    timestepper = PositionVerlet()
    do_step, stages_and_updates = extend_stepper_interface(timestepper, Uniform_M_Sim)
    
    return do_step, stages_and_updates, timestepper, M_rod, MR_list 
