import pygame, os
import numpy as np
import warnings
from utils import draw_text
import matplotlib.pyplot as plt

class OneEndFixed_screen_setting:
    
    def __init__(self,Screen_W, Screen_H, wall_length = 100, bar_length = 100,magnetic_ampiltude_max = 60e3):
        self.magnetic_amplitude_max = magnetic_ampiltude_max
        self.Screen_W = Screen_W
        self.Screen_H = Screen_H
        self.wall_length = wall_length
        self.bar_length = bar_length
        warnings.warn(
        "OneEndFixed_screen_setting is deprecated and included to screen_setting. The deprecated name will be removed in the future.",
        DeprecationWarning,
    )

    
    def init(self, current_dir):
        '''
        initiate pygame screen
        current_dir: the folder where logo icon locates 
        '''
        logo = pygame.image.load(current_dir + '/' + 'Qubot_Logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption("M Rod Real Time Sim")
        self.clock = pygame.time.Clock()

        # create a surface on screen
        self.screen = pygame.display.set_mode((self.Screen_W,self.Screen_H))
        self.canvas = pygame.Surface((self.Screen_W,self.Screen_H))
        self.font = pygame.font.SysFont("Arial",30)
        
        #--------logo in screen and wall display--------
        self.logo_S = pygame.image.load(current_dir + '/' + 'Qubot_Logo_S.png')
        
        self.wall_start_point = np.array([self.Screen_W//15 ,self.Screen_H//2 - self.wall_length//2]) # wall starting point
        self.wall_end_point = np.array([self.Screen_W//15 ,self.Screen_H//2 + self.wall_length//2])
        
        
        self.arrow_centra = np.array([self.Screen_W-80, 225])

        # amplitude bar
        bar_x = self.Screen_W - 200
        bar_y = 275
        self.bar_pos = np.array([bar_x, bar_y])
        self.bar_ratio = self.magnetic_amplitude_max/self.bar_length
    
    def draw(self, rods, magnetic_amplitude, magnetic_field_direction, normal_direction, width, fps, tri_size =10):
        '''
        draw rod configuration and bar and magnetic_direction
        -----------------------------
        Input:
        rods: tuple, pyelastica rod objects
        tri_size: arrow triangle size
        '''
        self.canvas.fill((255,255,255))
        # draw wall
        pygame.draw.line(self.canvas, 'black', self.wall_start_point,self.wall_end_point, width=3)
        self.canvas.blit(self.logo_S, (self.Screen_W-80,25))

        # draw arrow
        rotate_matrix = np.array([[1.0,0.0],[0.0,-1.0]]) # since pygame's origin start in left up corner, we have to rotate the coordinate
        normal_direction = rotate_matrix@normal_direction
        arrow_end = self.arrow_centra +rotate_matrix@magnetic_field_direction[1:]*self.wall_length/2
        arrow_start = self.arrow_centra -rotate_matrix@ magnetic_field_direction[1:]*self.wall_length/2
        pygame.draw.line(self.canvas, "black",arrow_start, arrow_end, width=2)
        pygame.draw.polygon(self.canvas, "black", [arrow_end + tri_size*normal_direction , arrow_end-tri_size*normal_direction, arrow_end + tri_size*rotate_matrix@magnetic_field_direction[1:]*np.sqrt(3)])

        # draw amplitude bar 
        bar_hight = np.array([0, magnetic_amplitude/self.bar_ratio])
        pygame.draw.polygon(self.canvas, "darkgray", (self.bar_pos, self.bar_pos + np.array([23,0]),  self.bar_pos + np.array([23,0])- bar_hight, self.bar_pos-bar_hight))
        pygame.draw.rect(self.canvas,"black",(self.bar_pos[0],self.bar_pos[1]-self.bar_length,25, self.bar_length),4)

        self.screen.blit(self.canvas,(0,0))
        draw_text(self.screen, f"{magnetic_amplitude*1e-3:.0f} mT", "black", x=self.bar_pos[0], y= self.bar_pos[1], font=self.font)
        # draw rod
        # rescale rod pos to large pixels rod and rotate the coordinate
        
        rescale_pos = 100*rotate_matrix@ rods.position_collection[1:] + (self.wall_start_point+self.wall_end_point).reshape(-1,1) /2
        rod_pos = [(rescale_pos[0,i], rescale_pos[1,i]) for i in range(rescale_pos.shape[-1])]
        pygame.draw.lines(self.screen, 'black', closed=False, points = rod_pos, width= width)
        self.clock.tick(fps)
        pygame.display.update()

#----------------------------------------
class screen_setting:
    
    def __init__(self, current_dir, Screen_W, Screen_H, bar_length = 100,magnetic_ampiltude_max = 60e3):
        self.magnetic_amplitude_max = magnetic_ampiltude_max
        self.Screen_W = Screen_W
        self.Screen_H = Screen_H
        self.bar_length = bar_length

        '''
        initiate pygame screen
        current_dir: the folder where logo icon locates 
        '''
        logo = pygame.image.load(current_dir + '/' + 'Qubot_Logo.png')
        pygame.display.set_icon(logo)
        pygame.display.set_caption("M Rod Real Time Sim")
        self.clock = pygame.time.Clock()

        # create a surface on screen
        self.screen = pygame.display.set_mode((self.Screen_W,self.Screen_H))
        self.canvas = pygame.Surface((self.Screen_W,self.Screen_H))
        self.font = pygame.font.SysFont("Arial",30)
        
        #--------logo in screen and bar display--------
        # logo
        self.logo_S = pygame.image.load(current_dir + '/' + 'Qubot_Logo_S.png')

        # amplitude bar
        bar_x = self.Screen_W - 200
        bar_y = 275
        self.bar_pos = np.array([bar_x, bar_y])
        self.bar_ratio = self.magnetic_amplitude_max/self.bar_length

        # arrow
        self.arrow_centra = np.array([self.Screen_W-80, 225])

        # constraint position
        self.constraint_centra = np.array([self.Screen_W//15 ,self.Screen_H//2])

    def OneEndFixedDraw(self, wall_length = 100):
        self.wall_start_point = self.constraint_centra + np.array([0 , - wall_length//2]) # wall starting point
        self.wall_end_point = self.constraint_centra + np.array([0 , wall_length//2])


        # draw wall
        pygame.draw.line(self.canvas, 'black', self.wall_start_point,self.wall_end_point, width=3)
        self.canvas.blit(self.logo_S, (self.Screen_W-80,25))
        
    def ActuatorDraw(self, tri_length=20):
        pygame.draw.polygon(self.canvas, "black", [self.constraint_centra , self.constraint_centra + np.ones(2)*tri_length, self.constraint_centra + np.array([-1,1])*tri_length])
        pygame.draw.polygon(self.canvas, "black", [self.constraint_centra , self.constraint_centra - np.ones(2)*tri_length, self.constraint_centra - np.array([-1,1])*tri_length])

        
    def SpeedometerDraw(self, actuator_velocity_omega):
       draw_text(self.screen, f"v: {actuator_velocity_omega[0]:.1f} mm/s", "black", x=self.bar_pos[0], y= self.bar_pos[1]-180, font=self.font) 

       draw_text(self.screen, f"\u03C9: {actuator_velocity_omega[1]:.1f} rad/s", "black", x=self.bar_pos[0], y= self.bar_pos[1]-150, font=self.font) 
    
    def draw(self,rods,magnetic_amplitude, magnetic_field_direction, normal_direction, width, fps, tri_size =10, arrow_length = 100, constraint = 'OneEndFixed', actuator_velocity_omega = None):
        '''
        draw rod configuration and bar and magnetic_direction
        M_rod: pyelastica rod object
        tri_size: arrow triangle size
        '''
        self.canvas.fill((255,255,255))
        # add logo
        self.canvas.blit(self.logo_S, (self.Screen_W-80,25))
        # draw constraint configuration
        if constraint == 'OneEndFixed':
            self.OneEndFixedDraw()
        elif constraint == 'Actuator':
            self.ActuatorDraw()

        # draw arrow
        rotate_matrix = np.array([[1.0,0.0],[0.0,-1.0]]) # since pygame's origin start in left up corner, we have to rotate the coordinate
        normal_direction = rotate_matrix@normal_direction
        arrow_end = self.arrow_centra +rotate_matrix@magnetic_field_direction[1:]*arrow_length/2
        arrow_start = self.arrow_centra -rotate_matrix@ magnetic_field_direction[1:]*arrow_length/2
        pygame.draw.line(self.canvas, "black",arrow_start, arrow_end, width=2)
        pygame.draw.polygon(self.canvas, "black", [arrow_end + tri_size*normal_direction , arrow_end-tri_size*normal_direction, arrow_end + tri_size*rotate_matrix@magnetic_field_direction[1:]*np.sqrt(3)])

        # draw amplitude bar 
        bar_hight = np.array([0, magnetic_amplitude/self.bar_ratio])
        pygame.draw.polygon(self.canvas, "darkgray", (self.bar_pos, self.bar_pos + np.array([23,0]),  self.bar_pos + np.array([23,0])- bar_hight, self.bar_pos-bar_hight))
        pygame.draw.rect(self.canvas,"black",(self.bar_pos[0],self.bar_pos[1]-self.bar_length,25, self.bar_length),4)

        self.screen.blit(self.canvas,(0,0))
        draw_text(self.screen, f"{magnetic_amplitude*1e-3:.0f} mT", "black", x=self.bar_pos[0], y= self.bar_pos[1], font=self.font)
        # draw speedometer
        if constraint == 'Actuator':
            self.SpeedometerDraw(actuator_velocity_omega)
        # draw rod
        # rescale rod pos to large pixels rod and rotate the coordinate
        for rod in rods:
            rescale_pos = 20*rotate_matrix@ rod.position_collection[1:] + (self.constraint_centra).reshape(-1,1) 
            rod_pos = [(rescale_pos[0,i], rescale_pos[1,i]) for i in range(rescale_pos.shape[-1])]
            pygame.draw.lines(self.screen, 'black', closed=False, points = rod_pos, width= width)
        self.clock.tick(fps)
        pygame.display.update()