#!/usr/bin/env python
# license removed for brevity

__author__ = 'jacques saraydaryan'

import pygame
import random
import os
import math
import numpy as np
from common.Particle import Particle
from Particle_Filter import Particle_Filter
from common.ToolBox import distance_to_obstacle,distance_to_obstacle_coord,std



class PlaneSimulation:
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED = [255, 0, 0]
    GREEN = [0, 255, 255]
    GREEN_light = [0, 255, 72,0.5]
    GREY_light = [183, 179, 179]
    GREEN_GREEN = [0, 255, 0]
    RED = [255, 0, 0]
    BLUE=[0, 0, 255]

    OBSTACLE = 100

    height = 720
    width = 1280

    LEFT_CLICK = 1
    RIGHT_CLICK = 3

    # Set the height and width of the screen
    SIZE = [width, height]
    # SCALE= 1
    SCALE = 10

    Y_INCREMENT_STEP=2

    particleFilter=""
    obs_grid=""
    entropy_min=500
    entropy_max=0
    entropylist=[]
    std_min=500
    std_max=0
    stdlist=[]
    plane_track=[]

    def __init__(self):
        grid_temp = self.load_obs_matrix("/tmp/", "obstacle.npy")
        self.command_x = 1 * self.SCALE
        self.command_y = 0
        
        if len(grid_temp) == 0:
            self.obs_grid = [[0 for x in range(int(round(self.width / self.SCALE)))] for y in range(int(round(self.height / self.SCALE)))]
        else:
            self.obs_grid = grid_temp
        self.particleFilter=Particle_Filter(self.width,self.height,self.obs_grid)
        
        self.particleFilter.resetParticle()


    # --------------------------------------------------------------------------------------------
    # ---------------------------------------- PYGAME LOOP ---------------------------------------
    # --------------------------------------------------------------------------------------------
    def startPyGameLoop(self):
        # Initialize the game engine
        pygame.init()

        screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Particle filter")


        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.myfont = pygame.font.SysFont("monospace", 15)

        # load image
        # player_image = pygame.image.load("./img/player.png").convert()

        player_image_not_scaled = pygame.image.load(os.path.dirname(__file__) + "/img/plane_nptrans.png").convert()
        player_image = pygame.transform.scale(player_image_not_scaled, (int(round(self.width / 10)), int(round(self.height / 10))))

        player_image_alpha=player_image.copy()
        alpha = 60
        player_image_alpha.set_alpha(alpha)
        clock = pygame.time.Clock()
        clicked_zone = []
        obstacles_list=[]


        plane_pose = {'x': 0, 'y': Particle_Filter.FIXED_PLANE_Y + 50}

        # Loop until the user clicks the close button.
        done = False
        isButtonPressed = False
        is_in_pause = True
        is_step_by_step = False
        step=0
        while not done:
            # ----------------------------------------------------------------------------------------------------------------
            # ----------------------------------------- USER UI EVENTS MNG  --------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------------
            for event in pygame.event.get():  # User did something
                # get event
                if event.type == pygame.QUIT:
                    done = True
                    print('end')
                # User pressed down on a key
                elif event.type == pygame.KEYDOWN:
                    print("down")
                    if event.key == pygame.K_RIGHT:
                        print('key Right pressed')
                        is_step_by_step = True
                    if event.key == pygame.K_UP:
                        if plane_pose['y']-self.Y_INCREMENT_STEP >=0 and plane_pose['y']-self.Y_INCREMENT_STEP < self.height:
                            #plane_pose['y']= plane_pose['y']-self.Y_INCREMENT_STEP*self.SCALE
                            self.command_y=-self.Y_INCREMENT_STEP*self.SCALE
                        print('key UP pressed')
                    if event.key == pygame.K_DOWN:
                        if plane_pose['y']+self.Y_INCREMENT_STEP >=0 and plane_pose['y']+self.Y_INCREMENT_STEP < self.height:
                            #plane_pose['y']= plane_pose['y']+self.Y_INCREMENT_STEP*self.SCALE
                            self.command_y=self.Y_INCREMENT_STEP*self.SCALE
                        
                        print ('key DOWN pressed')
                    if event.key == pygame.K_s:
                        print ('key s pressed')
                        self.save_obs_matrix("/tmp/", "obstacle.npy", self.obs_grid )

                    elif event.key == pygame.K_SPACE:
                        if is_in_pause:
                            is_in_pause = False
                        else:
                            is_in_pause = True
                    elif event.key == pygame.K_r:
                        #plane_pose['x'] = 0
                        plane_pose = {'x': 0, 'y': Particle_Filter.FIXED_PLANE_Y + 50}
                        self.entropy_min=500
                        self.entropy_max=0
                        self.entropylist=[]
                        self.stdlist=[]
                        plane_track=[]
                        self.std_min=500
                        self.std_max=0
                        self.particleFilter.resetParticle()
                    elif event.key == pygame.K_KP_PLUS:
                        self.command_x+=1*self.SCALE 
                        #self.particleFilter.increment += 1

                    elif event.key == pygame.K_KP_MINUS:
                        if self.particleFilter.increment > -1:
                            self.command_x-=1*self.SCALE
                            #self.particleFilter.increment -= 1


                # handle MOUSEBUTTONUP
                elif event.type == pygame.MOUSEBUTTONUP:
                    clicked_pos = pygame.mouse.get_pos()
                    clicked_zone.append(clicked_pos)
                    obstacles_list.append(clicked_pos)
                    isButtonPressed = False
                    current_click = 0

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    isButtonPressed = True
                    current_click = event.button
                    print ('click type' + str(event.button))

                if isButtonPressed:
                    clicked_pos = pygame.mouse.get_pos()

                    if int(round(self.width / self.SCALE)) > int(round(clicked_pos[0] / self.SCALE)) and int(round(self.height / self.SCALE)) > int(round(clicked_pos[
                        1] / self.SCALE)):
                        if current_click == self.LEFT_CLICK:
                            self.obs_grid[int(round(clicked_pos[1] / self.SCALE))][
                                int(round(clicked_pos[0] / self.SCALE))] = 100
                            print('obs--:' + str(clicked_pos[1]) + ',' + str(clicked_pos[0]))
                        elif current_click == self.RIGHT_CLICK:
                            self.obs_grid[int(round(clicked_pos[1] / self.SCALE))][
                                int(round(clicked_pos[0] / self.SCALE))] = 0
                            # Process each obstacles in the list
            # Set the screen background
            screen.fill(self.WHITE)

            # Game logic
            # get current mouse position
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            # render text
            label = self.myfont.render("(" + str(plane_pose['x']) + "," + str(plane_pose['y']) + ")", 1, (0, 0, 0))
            label1 = self.myfont.render("(" +str(x) + "," + str(y)+ ")", 1, (0, 0, 0))
            screen.blit(label, (0, 0))
            
            w,h = player_image_alpha.get_size()
            #print plane track
            for coord in  self.plane_track:
                pygame.draw.circle(screen, self.GREEN, [coord['x'], coord['y']], 5)
            screen.blit(player_image, [plane_pose['x']-50, plane_pose['y'] - 50])
            pygame.draw.circle(screen, self.GREEN, [plane_pose['x'], plane_pose['y']], 10)
            
            for i in range(len(clicked_zone)):
                # render text
                clicklab = self.myfont.render("(" + str(clicked_zone[i][0]) + "," + str(clicked_zone[i][1]) + ")", 1,
                                         (255, 255, 0))
            # Process each particule in the list
            for i in range(len(self.particleFilter.particle_list)):
               
                center = [self.particleFilter.particle_list[i].x, self.particleFilter.particle_list[i].y]
                radius = int(round(100 * self.particleFilter.particle_list[i].proba * len(self.particleFilter.particle_list) / 10))
                self._draw_circle(screen,self.GREEN_light,self.BLACK,center,radius,1)

            # ----------------------------------------------------------------------------------------------------------------
            # ----------------------------------------- COMPUTED PARTICULE FILTER ---------------------------------------------
            # ----------------------------------------------------------------------------------------------------------------
            if not is_in_pause or is_step_by_step:
                self.particleFilter.updateParticle(plane_pose, self.command_x, self.command_y)
                plane_pose['x'] = plane_pose['x'] + self.command_x
                plane_pose['y'] = plane_pose['y'] + self.command_y
                self.command_y = 0
            
            std_value=std(self.particleFilter.particle_list)
            self._draw_entropy(screen,std_value, False if (not is_in_pause or is_step_by_step) else True )
            
           
            try:
                distance_to_plane,cell_x,cell_y=distance_to_obstacle_coord(plane_pose['x'],plane_pose['y'],self.obs_grid,self.width,self.height,self.SCALE)
                label_distance = self.myfont.render("%.2f" % (distance_to_plane), 1, (0, 0, 0))
                screen.blit(label_distance, (plane_pose['x'], plane_pose['y']+int(round(abs(plane_pose['y']-cell_y)/2))))
                pygame.draw.line(screen, self.GREEN, (plane_pose['x'], plane_pose['y']),(cell_x,cell_y), 1)
            except TypeError:
                print("no value available for display")
            
            # ----------------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------------
            # Process each obstacles in the list
            # for i in range(len(obstacles_list)):
            #     pygame.draw.rect(screen, self.BLACK, [obstacles_list[i][0], obstacles_list[i][1], 10, 10])
            for y_i in range(len(self.obs_grid)):
                for x_j in range(len(self.obs_grid[0])):
                    if self.obs_grid[y_i][x_j] == self.OBSTACLE:
                        distance_to_line=distance_to_obstacle(x_j * self.SCALE,plane_pose['y'],self.obs_grid,self.width,self.height,self.SCALE)
                        if(distance_to_plane ==distance_to_line):
                            pygame.draw.rect(screen, self.GREEN,
                                             [x_j * self.SCALE,y_i * self.SCALE , self.SCALE, self.SCALE])
                        else:
                            pygame.draw.rect(screen, self.RED, [x_j * self.SCALE, y_i * self.SCALE, self.SCALE, self.SCALE])
        
        #Compute and draw cluster
        #particules_indices
        #for particule in self.particleFilter.particule_list:
            #TODO

                if step%10 ==0 :
                    coord={}
                    coord['x']=plane_pose['x']
                    coord['y']=plane_pose['y']
                    self.plane_track.append(coord)


            is_step_by_step = False
            step=step+1
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # clock.tick(20)
            clock.tick(100)

        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()

    def adjustFileName(self, file_path, file_name_prefix, file_name_sufix):
        if (os.path.isfile(file_path + '0-' + file_name_prefix + file_name_sufix)):
            index = 1
            while os.path.isfile(file_path + str(index) + '-' + file_name_prefix + file_name_sufix):
                index = index + 1
            return file_path + str(index) + '-' + file_name_prefix
        else:
            return file_path + '0-' + file_name_prefix

    def save_obs_matrix(self,filePath, fileName, matrix):
        # file=adjustFileName(filePath,fileName,matrix,'obs.data.npy')
        file = filePath + fileName
        np.save(file, matrix)

    def load_obs_matrix(self,filePath, fileName):
        if os.path.isfile(filePath + fileName):
            # return np.load(filePath + fileName)
            return np.asarray(np.load(filePath + fileName))
        else:
            return []

    def _load_param(self,config, param_name, variable):
        try:
            value=config[param_name]
            setattr( self.particleFilter, variable,value)

            print("parameter [%s] loaded with value [%s]"%(param_name,str(config[param_name])))
        except KeyError as e:
            print("Unable to load parameter from config file: "+str(e))

    def _draw_circle(self,screen, fill_color,border_color, center, radius, border_with):
        pygame.draw.circle(
                    screen, 
                    border_color, 
                    center, 
                    radius, 
                border_with
            )
        pygame.draw.circle(
                screen, 
                fill_color, 
                center, 
                radius - border_with, 
                0
            )
        
    def _draw_entropy(self,screen, std_value, in_pause=False):
        if not in_pause:
            self.stdlist.append(std_value)
        if self.std_min > std_value:
            self.std_min=std_value
        if self.std_max < std_value:
            self.std_max=std_value
        # Display entropy history
        std_cum=0
        
        for i in range (0, len(self.stdlist)):
            if math.isnan(self.stdlist[i]):
                break
            std_cum=self.stdlist[i]+std_cum
            pygame.draw.circle(screen, self.GREY_light, (i,int(round((self.stdlist[i]-1)*10))+25), 2)
        # Avoid /0
        if len(self.stdlist)-1 <=0 :
            return
        
        #Display line min max avg
        pygame.draw.line(screen, self.GREEN_GREEN, (0,int(round((self.std_min-1)*10))+25) ,(self.width,int(round((self.std_min-1)*10))+25), 1)
        pygame.draw.line(screen, self.RED, (0,int(round((self.std_max-1)*10))+25) ,(self.width,int(round((self.std_max-1)*10))+25), 1)
        pygame.draw.line(screen, self.BLUE, (0,int(round((std_cum/len(self.stdlist)-1)*10))+25) ,(self.width,int(round((std_cum/len(self.stdlist)-1)*10))+25), 1)
        label_std = self.myfont.render("STD DEVIATION:%.2f, MIN: %.2f, MAX: %.2f, AVG: %.2f" % (std_value,self.std_min,self.std_max,std_cum/len(self.stdlist)), 1, (0, 0, 0))
        screen.blit(label_std, (150, 0))




# COMMAND TYPE
# S key save the current obstacle map to /tmp/obstacle.npy
# R key reset the plane position and particule efilter
# + increase plane speed
# - decrease plane speed
# SPACE pause/resume
# Up move the plane up
# Down move the plane down
# Right when pause activated step by step
    
if __name__ == '__main__':
    pl_simulator=PlaneSimulation()
    pl_simulator.startPyGameLoop()






