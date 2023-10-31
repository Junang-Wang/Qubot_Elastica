import pygame
import numpy as np
import json, os 
from utils import *
from elastica.modules import BaseSystemCollection, Constraints, Forcing, Damping 
from elastica import CallBacks
from Uniform_Magnetic_Rod import Sim_init, magnetic_amplitude, magnetic_field_direction

def main():
    global magnetic_amplitude, magnetic_field_direction
#------------------icon and screen setting ----------
    pygame.init()
    Screen_W, Screen_H = 960, 570
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
    wall_start_point = np.array([Screen_W//15 ,Screen_H//2 - wall_length//2]) # wall starting point
    wall_end_point = np.array([Screen_W//15 ,Screen_H//2 + wall_length//2])
    
    
    arrow_start = np.array([Screen_W-80, 225])
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
    dt = 1.4e-4
    time = 0
    do_step, stages_and_updates, timestepper, M_rod = Sim_init(Uniform_M_Sim, dt=dt)

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
        rescale_pos = 100*M_rod.position_collection[1:] + (wall_start_point+wall_end_point).reshape(-1,1) /2
        rod_pos = [(rescale_pos[0,i], rescale_pos[1,i]) for i in range(rescale_pos.shape[-1])]
        pygame.draw.lines(screen, 'black', closed=False, points = rod_pos)
        clock.tick(60)
        pygame.display.update()
        
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
