import pygame
import time
import sys
import copy
import os
from settings import *
from player_class import *
from enemy_class import *
import random ,time
from button import *




pygame.init()
vec = pygame.math.Vector2


class App:

    def __init__(self,mapfile):
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.caption = pygame.display.set_caption("Pacman algorithm")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coinss = []
        self.coins = []
        self.coinstmp = []
        self.enemies = []
        self.e_poss = []
        self.e_pos = []
        self.p_pos = None
        self.count = 0
        self.load(mapfile)
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
        self.path = []
        self.start_time = 0
        self.current_time = 0
        self.running_time = 0
        self.pre_direction = vec(0,0)
        self.wallsname = ["walls.txt","walls2.txt","walls3.txt","walls4.txt","walls5.txt","walls6.txt","walls7.txt","walls8.txt","walls9.txt","walls10.txt"]
        
    #2 ham tao map toi che ra nhung no deo chay  
    '''def select_map_draw(self):
        self.screen.blit(pygame.image.load("assets/Background.png"), (0, 0))
        MAP1 = pygame.image.load("walls/walls1.png")
        self.screen.blit(MAP1, MAP1.get_rect(center=(20, 260)))
        pygame.display.update()

    def select_map(self):
        self.draw_text('Select your map that you want', self.screen, [ WIDTH//2, HEIGHT//2+100],
                       START_TEXT_SIZE, (100, 167, 198), START_FONT ,centered = True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 :
                    
                if event.key == pygame.K_2 :

        pygame.display.update()'''
    def run(self):
        self.start_time = time.time()
        while self.running:
            if self.state == 'start':
                
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                
                direction  = self.player.get_path_direction(self.coins[0])
                self.player.move(direction)      
                self.current_time = time.time()
                self.running_time = round(self.current_time - self.start_time, 2)
                self.playing_update()
                self.playing_draw()
                

                
            elif self.state == 'game over':
                
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################ HELPER FUNCTIONS ##################################

    def draw_text(self, words, screen, pos, size, colour, font_name = "assets/font.ttf", centered=False):
        font = pygame.font.Font(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self,mapfile):
        #self.select_map_draw()
        #self.select_map()

        self.background = pygame.image.load('E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\wall.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        
       
        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open(mapfile, 'r') as file:
        
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))
                        self.coinss.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char == "2":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                self.cell_width, self.cell_height))
                        self.e_poss.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))
            self.coins.append(random.choice(self.coinss))
            self.coinstmp = self.coins
            self.e_pos = random.sample(self.e_poss, 7)
            #print(self.e_poss)
            
    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    
    def reset(self):
        self.player.lives = 1
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        if(self.count%2 != 0):
            self.enemies = []
            self.e_pos = random.sample(self.e_poss,7)
            self.make_enemies()

        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
        
        if(self.count == 0):
            self.coins = self.coinstmp
        elif(self.count % 2 == 0):
            self.coins = self.coinstmp
        elif(self.count % 2 != 0):
            self.coins = []
            self.coins.append(random.choice(self.coinss))
            self.coinstmp = self.coins

        if(self.player.state == 'bfs'):

            print(self.player.nodes,"node ---> astar ")
            print(self.running_time,"s ---> astar")

        if(self.player.state == 'astar'):           
            print(self.player.nodes,"node ---> bfs")
            print(self.running_time,"s ---> bfs")
        self.start_time = time.time()
        self.running_time = 0
        self.player.nodes = 0
        self.player.index = 0
        self.shortest = []
        if self.player.state == 'bfs' :
            self.player.shortest = self.player.BFS(self.p_pos, self.coins[0])
        elif self.player.state == 'astar' :
            self.player.shortest = self.player.ASTAR(self.p_pos, self.coins[0])
        self.player.next = self.p_pos
        self.player.index = 0
        self.state = "playing"
        self.count += 1


########################### INTRO FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_1 :
                    self.state = 'playing'
                    self.player.state = 'bfs'
                    self.player.shortest = self.player.BFS(self.p_pos, self.coins[0])
                if event.key == pygame.K_2 :
                    self.state = 'playing'
                    self.player.state ='astar'
                    self.player.shortest = self.player.ASTAR(self.p_pos, self.coins[0])

    def start_update(self):
        pass




    def start_draw(self):  
        self.screen.blit(pygame.image.load("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\assets\Background.png"), (0, 0))
        self.caption
        self.draw_text('CHOOSE ONE PLAY OPTION', self.screen, [
                       WIDTH//2, HEIGHT//2-40], 50 , "#b68f40", "assets/font.ttf", centered=True)
        self.draw_text('1 BFS', self.screen, [ WIDTH//2, HEIGHT//2+100],
                       35, "#b68f40", "assets/font.ttf" ,centered = True)
        self.draw_text('2 A_STAR', self.screen, [ WIDTH//2, HEIGHT//2+180],
                       35, "#b68f40", "assets/font.ttf" ,centered = True)
        pygame.display.update()

########################### PLAYING FUNCTIONS ##################################


    
    def playing_update(self):    
        self.player.update()
        
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                if(self.player.state == 'bfs'):
                    print("ERROR astar")
                elif(self.player.state == 'astar'):
                    print("ERROR bfs")
                self.remove_life()      
        
    def playing_draw(self):
        
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()

        self.draw_text('RUNNING TIME: {:.2f}'.format(self.running_time),
                       self.screen, [60, 0], 14, WHITE, "assets/font.ttf")
        self.draw_text('NODES: {}'.format(self.player.nodes), self.screen, [WIDTH//2+60, 0], 14, WHITE, "assets/font.ttf")
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
         
        pygame.display.flip()
        

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)
        if self.coins == [] :
            self.state = "game over"

########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
              #  self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        if(self.player.state == "bfs"):
            again_text = "Press SPACE bar to PLAY BFS"
        elif(self.player.state == "astar"):
            again_text = "Press SPACE bar to PLAY ASTAR"
            
        self.screen.blit(pygame.image.load("assets/Background.png"), (0, 0))
        quit_text = "Press the escape button to QUIT"
        #again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100],  52, RED, "assets/font.ttf", centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  36, (190, 190, 190), "assets/font.ttf", centered=True)

        self.draw_text("RUNNING TIME : " + str(self.running_time), self.screen ,[WIDTH//2, 222], 36, (190,190,190),"assets/font.ttf", centered = True)
        self.draw_text("NODES : " + str(self.player.nodes), self.screen ,[WIDTH//2, 262], 36, (190,190,190),"assets/font.ttf", centered = True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "assets/font.ttf", centered=True)
        pygame.display.update()
        
