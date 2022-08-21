import pygame
import random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.speed = 2
        self.num = 0


    def update(self):
        self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            self.move()


        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)
        #pygame.draw.rect(self.app.screen, self.colour, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    
    def move(self):
        self.direction = self.get_direction()
    

    def get_direction(self):
        #global number
        #self.num = 0
        while True :
            #number = random.randint(-2, 1)
            if self.num % 2 == 0:
                x_dir, y_dir = -1, 0
            elif self.num % 2 == 1:
                x_dir, y_dir = 1, 0
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
        
            if next_pos not in self.app.walls  :
                return vec(x_dir, y_dir)
            else :
                self.num += 1

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 +
                   self.app.cell_height//2)

    def set_colour(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)
        if self.number == 4:
            return (43, 78, 203)
        if self.number == 5:
            return (197, 200, 27)
        if self.number == 6:
            return (189, 29, 29)
        if self.number == 7:
            return (215, 159, 33)

