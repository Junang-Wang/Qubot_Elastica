import sys,os 
sys.path.append("./PyElastica_Playground")
# sys.path.append(os.path.abspath('./PyElastica_Playground'))
from M_rod_packages import *
import Actuator_Rod
from Plot_Method import *
from utils import *
from Actuation_matrix_package.Actuation_function import Centra_actuation_function
def main(PID=True, video= True, joystick= True):
    global magnetic_field
    magnetic_amplitude = 0
    magnetic_field_direction = np.array([0.0,0.0,1.0])
    normal_direction = np.array([1.0,0.0]) # magnetic field normal direction in yz plane
    scale_E = 1e-3 # scale down Young's module and magnetic torque at the same time to prevent numerical problems
    magnetic_field = magnetic_field_direction*magnetic_amplitude * scale_E
    current_vec = np.zeros(6)
#------------------icon and screen setting ----------
    pygame.init()
    current_dir = os.path.dirname(__file__)
    Screen_W, Screen_H = 960, 1200
    wall_length = 100 # 100 pixes long wall
    bar_length = 100 # 100 pixes long magnetic amplitude bar
    magnetic_amplitude_max = 60e3
    my_screen_setting = screen_setting(current_dir, Screen_W, Screen_H, bar_length, magnetic_amplitude_max)
    # initiate screen in pygame 
    fps = 60
    running = True
#----------------PyElastica Simulator-------------
    class UnitMagneticRodSimulator(BaseSystemCollection, Constraints, Connections, Forcing, Damping, CallBacks):
        pass
    Uniform_M_Sim = UnitMagneticRodSimulator()
    dt = 1.4e-4 # time step
    time = 0
    frames_per_sec = int(1/60 / dt)
    frame = 0
    actuator_velocity_omega = np.array([0.,0])
    do_step, stages_and_updates, timestepper, S_rod, M_rod, M_list, S_list = Actuator_Rod.Sim_init(Uniform_M_Sim, magnetic_field, dt=dt, scale_E=scale_E, actuator_velocity_omega= actuator_velocity_omega)

    #-------------------plot time-dependent end position versus ref end position--------------------------
    # ref_position = np.array([0.0, 3.9457, 4.0515])
    ref_position = np.array([0.0, 0.0, 4.0515])
    

   #---------initialize controller----------------
    if joystick:
        PS4_joystick = pygame.joystick.Joystick(0)
        PS4_joystick.init()

    with open(os.path.join(current_dir,"ps4_keys.json"), 'r+') as file:
        PS4_keys = json.load(file)
    # 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
    # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
    analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 } 
#----------------main loop----------------------
    while running:
        for event in pygame.event.get():
            
            #--------define quit button----------
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == PS4_keys['x']:
                    running = False
                elif event.button == PS4_keys['L1']:
                    actuator_velocity_omega[1] += 1
                elif event.button == PS4_keys['R1']:
                    actuator_velocity_omega[1] -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if magnetic_amplitude < magnetic_amplitude_max:
                        magnetic_amplitude += 1e3
                elif event.key == pygame.K_DOWN:
                    if magnetic_amplitude >=1e3:
                        magnetic_amplitude -= 1e3
                
                if event.key == pygame.K_LEFT:
                    actuator_velocity_omega[0] -= 0.5
                elif event.key == pygame.K_RIGHT:
                    actuator_velocity_omega[0] += 0.5
                
                if event.key == pygame.K_1:
                    if current_vec[0] < 1:
                        current_vec[0] += 0.1
                elif event.key == pygame.K_a:
                    if current_vec[0] > -1:
                        current_vec[0] -= 0.1 
                
                if event.key == pygame.K_2:
                    if current_vec[1] < 1:
                        current_vec[1] += 0.1
                elif event.key == pygame.K_b:
                    if current_vec[1] > -1:
                        current_vec[1] -= 0.1

                if event.key == pygame.K_3:
                    if current_vec[2] < 1:
                        current_vec[2] += 0.1
                elif event.key == pygame.K_e:
                    if current_vec[2] > -1:
                        current_vec[2] -= 0.1  
                
                if event.key == pygame.K_4:
                    if current_vec[3] < 1:
                        current_vec[3] += 0.1
                elif event.key == pygame.K_r:
                    if current_vec[3] > -1:
                        current_vec[3] -= 0.1 

                if event.key == pygame.K_5:
                    if current_vec[4] < 1:
                        current_vec[4] += 0.1
                elif event.key == pygame.K_t:
                    if current_vec[4] > -1:
                        current_vec[4] -= 0.1 

                if event.key == pygame.K_6:
                    if current_vec[5] < 1:
                        current_vec[5] += 0.1
                elif event.key == pygame.K_y:
                    if current_vec[5] > -1:
                        current_vec[5] -= 0.1 
                
                if event.key == pygame.K_LEFTBRACKET:
                    actuator_velocity_omega[1] -= 0.5
                elif event.key == pygame.K_RIGHTBRACKET:
                    actuator_velocity_omega[1] += 0.5





            #update magnetic_field
            temp_magnetic_field = Centra_actuation_function(current_vec)
            
            magnetic_field[1] = temp_magnetic_field[0]*scale_E
            magnetic_field[2] = temp_magnetic_field[1]*scale_E

        #---------update rod and screen---------

        # update rod
        time = do_step(timestepper, stages_and_updates, Uniform_M_Sim, time, dt)
        frame += 1

        #PID controller
        current_pos = np.array([0.0,0.0,M_list["position"][-1][2,-1]])
        # current_pos = M_list["position"][-1][:,-1]
        
        #------------------------PID controller on of off ------------
        if PID:
            magnetic_amplitude, magnetic_field_direction = PIDController.calculate_magnetic_field(Kp=0.6*0.007, Ki= 1.2*0.02/0.28, Kd = 3*0.0001*0.28/400000, target_pos=ref_position, current_pos=current_pos, magnetic_field=magnetic_field, scale_E=scale_E,time_step=dt, magnetic_amplitude_max=magnetic_amplitude_max)
            normal_direction = np.array([-magnetic_field_direction[2],magnetic_field_direction[1]])

            plot_SISO_controller_performance([0,6], ref_position, M_list, figure_name=current_dir+"/M_rod_PID.jpg")
        

        
        if frame % frames_per_sec == 0:
            my_screen_setting.draw((S_rod, M_rod), magnetic_amplitude, magnetic_field_direction, normal_direction, width = 4, fps = fps, constraint = 'Actuator', actuator_velocity_omega=actuator_velocity_omega)
            # print(M_list["position"][-1][:,-1])
        if time >= 80:
            running = False
        
    if video:
        plot_video_2D(np.array([1.0,0.0,0.0]), [-2,35],[-5,30], S_list, M_list, video_name=current_dir+'/M_rod_Manual_soft.mp4',fps=20)
    


        
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    
    main(PID=False, video= False, joystick= False)
    
