from M_rod_packages import *
from Plot_Method import *
def main(PID=True):
    global magnetic_field
    magnetic_amplitude = 0
    magnetic_field_direction = np.array([0.0,0.0,1.0])
    normal_direction = np.array([1.0,0.0]) # magnetic field normal direction in yz plane
    scale_E = 1e-3 # scale down Young's module and magnetic torque at the same time to prevent numerical problems
    magnetic_field = magnetic_field_direction*magnetic_amplitude * scale_E
#------------------icon and screen setting ----------
    pygame.init()
    current_dir = os.path.dirname(__file__)
    Screen_W, Screen_H = 960, 1200
    wall_length = 100 # 100 pixes long wall
    bar_length = 100 # 100 pixes long magnetic amplitude bar
    magnetic_amplitude_max = 120e3
    my_screen_setting = OneEndFixed_screen_setting(Screen_W, Screen_H, wall_length, bar_length, magnetic_amplitude_max)
    my_screen_setting.init(current_dir) # initiate screen in pygame 
    fps = 60
    running = True
#----------------PyElastica Simulator-------------
    class UnitMagneticRodSimulator(BaseSystemCollection, Constraints, Forcing, Damping, CallBacks):
        pass
    Uniform_M_Sim = UnitMagneticRodSimulator()
    dt = 1.4e-4 # time step
    time = 0
    frames_per_sec = int(1/60 / dt)
    frame = 0
    do_step, stages_and_updates, timestepper, M_rod, M_list = Sim_init(Uniform_M_Sim, magnetic_field, dt=dt, scale_E=scale_E)

    #-------------------plot time-dependent end position versus ref end position--------------------------
    # ref_position = np.array([0.0, 3.9457, 4.0515])
    ref_position = np.array([0.0, 0.0, 4.0515])
    


#----------------main loop----------------------
    while running:

        #---------update rod and screen---------

        # update rod
        time = do_step(timestepper, stages_and_updates, Uniform_M_Sim, time, dt)
        frame += 1

        #PID controller
        current_pos = np.array([0.0,0.0,M_list["position"][-1][2,-1]])
        # current_pos = M_list["position"][-1][:,-1]
        
        #------------------------PID controller on of off ------------
        if PID:
            magnetic_amplitude, magnetic_field_direction = PIDController.calculate_magnetic_field(Kp=0.6*0.02, Ki= 1.2*0.02/0.28, Kd = 3*0.02*0.28/400000, target_pos=ref_position, current_pos=current_pos, magnetic_field=magnetic_field, scale_E=scale_E,time_step=dt, magnetic_amplitude_max=magnetic_amplitude_max)
            normal_direction = np.array([-magnetic_field_direction[2],magnetic_field_direction[1]])
        

        
        if frame % frames_per_sec == 0:
            my_screen_setting.draw(M_rod, magnetic_amplitude, magnetic_field_direction, normal_direction, width = 4, fps = fps)
            # print(M_list["position"][-1][:,-1])
        if time >= 4:
            running = False
    plot_SISO_controller_performance([0,6], ref_position, M_list, figure_name=current_dir+"/M_rod_PID.jpg")


        
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main(PID=True)
    
