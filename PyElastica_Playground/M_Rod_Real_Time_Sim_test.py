import pygame
import numpy as np
import json, os 
from utils import *
from elastica.modules import BaseSystemCollection, Constraints, Forcing, Damping 
from elastica import CallBacks
from PyElastica_Playground.M_rod_packages.Uniform_Magnetic_Rod import Sim_init
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Video
from elastica.modules import BaseSystemCollection, Constraints, Forcing, Damping 

from elastica.rod.cosserat_rod import CosseratRod 
from elastica.dissipation import AnalyticalLinearDamper
from elastica.boundary_conditions import OneEndFixedBC
from elastica.external_forces import EndpointForces, GravityForces 
from elastica import Connections
from elastica import FixedJoint
from elastica.callback_functions import CallBackBaseClass
from elastica.timestepper import integrate, PositionVerlet, extend_stepper_interface
from elastica import CallBacks

from elastica.timestepper.symplectic_steppers import PositionVerlet
from collections import defaultdict
from magneto_pyelastica import *

#------------------icon and screen setting ----------
pygame.init() #TODO Make the code concise and clear 
Screen_W, Screen_H = 960, 1200
current_dir = os.path.dirname(__file__)
logo = pygame.image.load(current_dir + '/' + 'Qubot_Logo.png')
pygame.display.set_icon(logo)
pygame.display.set_caption("M Rod Real Time Sim")
clock = pygame.time.Clock()

# create a surface on screen
screen = pygame.display.set_mode((Screen_W,Screen_H))
canvas = pygame.Surface((Screen_W,Screen_H))
font = pygame.font.SysFont("Arial",30)

#--------logo in screen and wall display--------
logo_S = pygame.image.load(current_dir + '/' + 'Qubot_Logo_S.png')

wall_length = 100
wall_start_point = np.array([Screen_W//3.5 ,Screen_H//2 - wall_length//2]) # wall starting point
wall_end_point = np.array([Screen_W//3.5 ,Screen_H//2 + wall_length//2])


arrow_start = np.array([Screen_W-80, 225])
M_configuration = [0, np.array([0.0,0.0,1.0])] # amplitude, direction
magnetic_amplitude = M_configuration[0]
magnetic_field_direction = M_configuration[1]
# magnetic_field_direction = np.array([0.0,1.0])
normal_direction = np.array([1.0,0.0])
# amplitude bar
bar_x = Screen_W - 200
bar_y = 275
bar_pos = np.array([bar_x, bar_y])
bar_length = 100
# magnetic_amplitude = 0
magnetic_amplitude_max = 60e3
bar_ratio = magnetic_amplitude_max/bar_length
running = True
#---------initialize controller----------------
PS4_joystick = pygame.joystick.Joystick(0)
PS4_joystick.init()

with open(os.path.join(current_dir,"ps4_keys.json"), 'r+') as file:
    PS4_keys = json.load(file)
# 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
# 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }

#----------------PyElastica Simulator-------------
class UnitMagneticRodSimulator(BaseSystemCollection, Constraints, Forcing, Damping, CallBacks):
    pass
Uniform_M_Sim = UnitMagneticRodSimulator()
time = 0
#--------mmGS unit----------
density = 2.273  #mg/mm^3 
base_length = 6 #mm 
base_radius = 0.3 #mm 
scale_E = 1e-3 #scale dowing Young's modulus
E = 1.4e9 * scale_E #Young's modulus
shear_modulus = E/3  # shear modulus


dt = 1.4e-4 # time step
nu = 7
endtime = 5000

#--------rod definition-------
n_elem = 40
start = np.array([0.0,0.0,0.0])
direction = np.array([0.0,1.0,0.0])
normal = np.array([1.0,0.0,0.0])
M_rod = CosseratRod.straight_rod(n_elem, start, direction, normal, base_length, base_radius, density, youngs_modulus=E, shear_modulus=shear_modulus)

Uniform_M_Sim.append(M_rod)
#--------magnetic properties-----
sclae_E_s = 1e2 # separate contribution of density and magnetic field
magnetization_density = 1.28e5 * 1e-3 * 1/sclae_E_s#A/mm
rescale_magnetic_amplitude = magnetic_amplitude*scale_E* sclae_E_s # mg/(s^2*A)

magnetization_direction = np.ones((n_elem)) * direction.reshape(3, 1)

#------set the constant magnetic field object-----
magnetic_field = rescale_magnetic_amplitude* magnetic_field_direction
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

#######################################################################  
#----------------main loop----------------------
while running:
    for event in pygame.event.get():
        #--------define quit button----------
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == PS4_keys['x']:
                running = False

        #-----------Analog Inputs----------
        if event.type == pygame.JOYAXISMOTION:
            analog_keys[event.axis] = event.value
        #---------right analog axis----------
            if abs(analog_keys[2]) > .4 or abs(analog_keys[3]) >.4:

                magnetic_field_direction = np.array([0.0,analog_keys[2], analog_keys[3]])
                magnetic_field_direction = magnetic_field_direction / np.linalg.norm(magnetic_field_direction)

                normal_direction = np.array([-magnetic_field_direction[2],magnetic_field_direction[1]])
        #--------left analog axis------------
            if abs(analog_keys[1]) >.3:
                if magnetic_amplitude <= magnetic_amplitude_max:
                    magnetic_amplitude -= analog_keys[1]*3e3
                if magnetic_amplitude >= magnetic_amplitude_max:
                    magnetic_amplitude = magnetic_amplitude_max
                if magnetic_amplitude < 0:
                    magnetic_amplitude = 0
            rescale_magnetic_amplitude = magnetic_amplitude*scale_E* sclae_E_s
            magnetic_field += rescale_magnetic_amplitude* magnetic_field_direction - magnetic_field # make sure using the same id(magnetic_field)

    

    #---------update rod and screen---------

    # update rod
    time = do_step(timestepper, stages_and_updates, Uniform_M_Sim, time, dt)

    canvas.fill((255,255,255))
    # draw wall
    pygame.draw.line(canvas, 'black', wall_start_point,wall_end_point, width=3)
    canvas.blit(logo_S, (Screen_W-80,25))

    # draw arrow
    arrow_end = arrow_start + magnetic_field_direction[1:]*wall_length/2
    tri_size = 10
    pygame.draw.line(canvas, "black",arrow_start - magnetic_field_direction[1:]*wall_length/2, arrow_end, width=2)
    pygame.draw.polygon(canvas, "black", [arrow_end + tri_size*normal_direction , arrow_end-tri_size*normal_direction, arrow_end + tri_size*magnetic_field_direction[1:]*np.sqrt(3)])

    # draw amplitude bar 
    bar_hight = np.array([0, magnetic_amplitude/bar_ratio])
    pygame.draw.polygon(canvas, "darkgray", (bar_pos, bar_pos + np.array([23,0]),  bar_pos + np.array([23,0])- bar_hight, bar_pos-bar_hight))
    pygame.draw.rect(canvas,"black",(bar_x,bar_y-bar_length,25, bar_length),4)

    screen.blit(canvas,(0,0))
    draw_text(screen, f"{magnetic_amplitude*1e-3:.0f} mT", "black", x=bar_x, y= bar_y, font=font)
    # draw rod
    rescale_pos =100*M_rod.position_collection[1:] + (wall_start_point+wall_end_point).reshape(-1,1) /2
    rod_pos = [(rescale_pos[0,i], rescale_pos[1,i]) for i in range(rescale_pos.shape[-1])]
    pygame.draw.lines(screen, 'black', closed=False, points = rod_pos, width=3)
    clock.tick(200)
    pygame.display.update()
        
