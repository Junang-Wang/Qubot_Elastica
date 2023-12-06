import numpy as np
from elastica import *
from magneto_pyelastica import *
from Actuator_package.Actuator_Constraint import ActuatorConstraint
def Sim_init(Actuator_M_Rod_Sim, magnetic_field, spatial_lim= ([],[0,1],[-1,1]),actuator_velocity_omega= np.array([0.4,0]), density = 2.273, base_length_s = 30, base_length_m = 6, base_radius = 0.3,scale_E=1e-3, E= 1.4e9, dt = 1.4e-4, nu =5, step_skip = 100):
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
    n_elem_m = 30
    n_elem_s = 60
    start_s = np.array([0.0,-25.0,0.0])  # silicone  rod
    direction = np.array([0.0,1.0,0.0])
    normal = np.array([1.0,0.0,0.0])
    start_m = start_s + direction * base_length_s


    S_rod = CosseratRod.straight_rod(n_elem_s, start_s, direction, normal, base_length_s, base_radius, density, youngs_modulus=E, shear_modulus=shear_modulus)
    M_rod = CosseratRod.straight_rod(n_elem_m, start_m, direction, normal, base_length_m, base_radius, density, youngs_modulus=E, shear_modulus=shear_modulus)

    Actuator_M_Rod_Sim.append(M_rod)
    Actuator_M_Rod_Sim.append(S_rod)
    #--------magnetic properties-----
    # sclae_E_s = 1e2 # separate contribution of density and magnetic field
    magnetization_density = 1.28e5 * 1e-3 #A/mm
    

    magnetization_direction = np.ones((n_elem_m)) * direction.reshape(3, 1)

    #------set the constant magnetic field object-----
    # rescale_magnetic_amplitude = magnetic_amplitude*scale_E # mg/(s^2*A)
    # magnetic_field = rescale_magnetic_amplitude* magnetic_field_direction

    magnetic_field_object = ConstantMagneticField(
        magnetic_field, ramp_interval = 0.1, start_time = 0, end_time = endtime
    )

    #--------constrain----------
    Actuator_M_Rod_Sim.constrain(S_rod).using(
        ActuatorConstraint, spatial_lim = spatial_lim, actuator_velocity_omega = actuator_velocity_omega,  
    )

    Actuator_M_Rod_Sim.connect(
        first_rod = S_rod, second_rod = M_rod, first_connect_idx = -1, second_connect_idx = 0
    ).using(FixedJoint, k= 1e6, nu =5, kt = 1e5, nut = 0)

    #--------damping------------
    Actuator_M_Rod_Sim.dampen(M_rod).using(
        AnalyticalLinearDamper, damping_constant = nu, time_step = dt
    )
    Actuator_M_Rod_Sim.dampen(S_rod).using(
        AnalyticalLinearDamper, damping_constant = nu, time_step = dt
    )
    #--------force--------------
    Actuator_M_Rod_Sim.add_forcing_to(M_rod).using(
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
                # self.callback_params["position"].append(system.position_collection.copy()[1:,1:].T) # capture yz plane and nodes start from 1
                # self.callback_params["velocity"].append(system.velocity_collection.copy()[1:,1:].T)
                # self.callback_params["omega"].append(system.omega_collection.copy()[1:].T)
                # self.callback_params['d'].append(system.director_collection.copy()[1:,1:].transpose(2,0,1).reshape(n_elem,-1))
                # self.callback_params['B_field'].append(np.ones((n_elem,1))*magnetic_field[np.newaxis,1:])
                return
    MR_list = defaultdict(list)
    # Actuator_M_Rod_Sim.collect_diagnostics(S_rod).using(
    #     MagneticRodCallBack, step_skip = step_skip, callback_params = MR_list
    # )
    Actuator_M_Rod_Sim.collect_diagnostics(M_rod).using(
        MagneticRodCallBack, step_skip = step_skip, callback_params = MR_list
    )

    Actuator_M_Rod_Sim.finalize()
    #--------time integration-----
    timestepper = PositionVerlet()
    do_step, stages_and_updates = extend_stepper_interface(timestepper, Actuator_M_Rod_Sim)
    
    return do_step, stages_and_updates, timestepper, S_rod, M_rod, MR_list 
