import pygame, os
import numpy as np
from utils import draw_text
class OneEndFixed_screen_setting:
    
    def __init__(self,Screen_W, Screen_H, wall_length = 100, bar_length = 100,magnetic_ampiltude_max = 60e3):
        self.magnetic_amplitude_max = magnetic_ampiltude_max
        self.Screen_W = Screen_W
        self.Screen_H = Screen_H
        self.wall_length = wall_length
        self.bar_length = bar_length

    
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
        
        
        self.arrow_start = np.array([self.Screen_W-80, 225])

        # amplitude bar
        bar_x = self.Screen_W - 200
        bar_y = 275
        self.bar_pos = np.array([bar_x, bar_y])
        self.bar_ratio = self.magnetic_amplitude_max/self.bar_length
    
    def draw(self,M_rod,magnetic_amplitude, magnetic_field_direction, normal_direction, width, fps, tri_size =10):
        '''
        M_rod: pyelastica rod object
        tri_size: arrow triangle size
        '''
        self.canvas.fill((255,255,255))
        # draw wall
        pygame.draw.line(self.canvas, 'black', self.wall_start_point,self.wall_end_point, width=3)
        self.canvas.blit(self.logo_S, (self.Screen_W-80,25))

        # draw arrow
        arrow_end = self.arrow_start + magnetic_field_direction[1:]*self.wall_length/2
    
        pygame.draw.line(self.canvas, "black",self.arrow_start - magnetic_field_direction[1:]*self.wall_length/2, arrow_end, width=2)
        pygame.draw.polygon(self.canvas, "black", [arrow_end + tri_size*normal_direction , arrow_end-tri_size*normal_direction, arrow_end + tri_size*magnetic_field_direction[1:]*np.sqrt(3)])

        # draw amplitude bar 
        bar_hight = np.array([0, magnetic_amplitude/self.bar_ratio])
        pygame.draw.polygon(self.canvas, "darkgray", (self.bar_pos, self.bar_pos + np.array([23,0]),  self.bar_pos + np.array([23,0])- bar_hight, self.bar_pos-bar_hight))
        pygame.draw.rect(self.canvas,"black",(self.bar_pos[0],self.bar_pos[1]-self.bar_length,25, self.bar_length),4)

        self.screen.blit(self.canvas,(0,0))
        draw_text(self.screen, f"{magnetic_amplitude*1e-3:.0f} mT", "black", x=self.bar_pos[0], y= self.bar_pos[1], font=self.font)
        # draw rod
        rescale_pos = 100*M_rod.position_collection[1:] + (self.wall_start_point+self.wall_end_point).reshape(-1,1) /2
        rod_pos = [(rescale_pos[0,i], rescale_pos[1,i]) for i in range(rescale_pos.shape[-1])]
        pygame.draw.lines(self.screen, 'black', closed=False, points = rod_pos, width= width)
        self.clock.tick(fps)
        pygame.display.update()